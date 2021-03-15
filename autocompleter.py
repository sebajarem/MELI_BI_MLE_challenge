# librerias de uso general
import json
import pickle
import pandas as pd
import numpy as np

# librerias de texto
import re
import nltk
from nltk import FreqDist
from nltk import word_tokenize, sent_tokenize

# transformer
from sentence_transformers import SentenceTransformer, util


DEFAULT_FILENAME = "autocompleter.pkl"


class Autocompleter:
    """
    clase autocompleter

    """
    def __init__(self):
        """
        inicializa objeto
        """
        self.conversations = None
        self.df_freq_frases = None
        self.df_freq_frases_ult_salida = None
        self.paraphrases = None

    def import_json(self, json_filename):
        """
        Lee archivo json, genera un DataFrame y lo guarda en el objeto

        :param json_filename: ruta+nombre_de_archivo json de entrada
        :type json_filename: str
        """
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            json_data = json.loads(json_file.read())

        # extraigo informacion de la lista Messages
        jsondf = pd.json_normalize(
            json_data,
            record_path=['Issues', 'Messages'],
            meta=[
                ['Issues', 'IssueId'],
                ['Issues', 'CompanyGroupId']
            ]
        )
        
        # casteo a 'str' por ser Ids
        jsondf['IssueId'] = jsondf['Issues.IssueId'].astype(str)
        jsondf['CompanyGroupId'] = jsondf['Issues.CompanyGroupId'].astype(str)
        jsondf = jsondf[['IssueId', 'CompanyGroupId', 'IsFromCustomer', 'Text']]

        # guardar la info en el objeto
        self.conversations = jsondf

    def conversations_agent(self):
        """
        De las conversaciones completas, se queda solamente con las conversaciones de los agentes

        :return: conversaciones exclusivamente de los agentes
        :rtype: pandas.core.frame.DataFrame
        """
        # se tienen en cuenta las frases de los agentes únicamente para recomendar en el autocompletado
        text_agent = self.conversations[self.conversations['IsFromCustomer'] == False]['Text'].reset_index()
        return text_agent

    def prepros_text(self):
        """
        limpieza y preproesamiento de texto.
        Guarda las frases con la frecuencia de aparicion

        """
        
        frases = '. '.join(self.conversations_agent()['Text'])
        frases = re.sub(r'[?]', '?.', frases)
        frases = sent_tokenize(frases)
        # convierto frase a lowercase
        frases = [s.lower() for s in frases]
        frases = re.split(r'[.,?]', ' '.join(frases))
        # elimino frases de 1 solo caracter
        frases = [s for s in frases if len(s) > 0]
        # limpieza para que la frase empiece con una letra
        frases = [ s if s[0] is not (' ' or '.' or ',' or '?') else s[1:]  for s in frases]
        
        # calculo de freq de las frases ordenado de mas frecuente a en os frecuente
        df_freq_frases = pd.DataFrame.from_dict(FreqDist(frases), orient='Index', columns=['freq'] ).sort_values('freq', ascending = False)
        df_freq_frases = df_freq_frases.reset_index()
        df_freq_frases.columns = ['frase', 'freq']

        # se guarda la info en el objeto
        self.df_freq_frases = df_freq_frases

        # limpio contexto
        del frases
        del df_freq_frases


    def sentence_similarity(self):
        """
        genera modelo de similaridad entre oraciones.
        Hace uso de Transformers con un modelo pre-entrenado en 
        procesamiento de lenguaje natural

        guarda las comparaciones entre oraciones con un score de similaridad
        NOTA: umbral definido en 100 en base a analisis y pruebas. Como mejora, podria parametrizarse.
        """
        # hecha la limpieza, me quedo con las frases que no son particulares de un caso
        sentences = list(self.df_freq_frases.frase[self.df_freq_frases.freq > 1])
        # utilizo el modelo pre-entrenado de analisis de texto con las frases a utilizar
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
        # genero matriz de similaridad entre las frases
        paraphrases = util.paraphrase_mining(model, sentences, top_k=100 )
        # guardo el modelo de similaridad
        self.paraphrases = paraphrases

    def generate_completions(self, prefix_string):
        """
        Genera las recomendaciones de oraciones basados en el texto inicial

        :param prefix_string: comienzo de texto a recomendar
        :type prefix_string: str
        :return: lista de oraciones recomendadas
        :rtype: list(str)
        """

        # hacer preprocesamiento si no se hizo antes
        if self.df_freq_frases is None:
            self.conversations_agent()
            self.prepros_text()
        
        # buscar patron en las frases y extraer desde el inicio del patron hasta el final de la frase
        self.df_freq_frases_ult_salida = self.df_freq_frases.copy()
        self.df_freq_frases_ult_salida['indice_coincide'] = self.df_freq_frases_ult_salida.frase.str.find(prefix_string)
        self.df_freq_frases_ult_salida['frase_salida'] = self.df_freq_frases_ult_salida.apply(lambda row: row.frase[row.indice_coincide:] if row.indice_coincide ==0 else '' , axis=1)
        self.df_freq_frases_ult_salida = self.df_freq_frases_ult_salida[self.df_freq_frases_ult_salida.frase_salida.apply(lambda x: len(x)>1)][['frase','frase_salida', 'freq']]
        self.df_freq_frases_ult_salida['indice_sentence'] = self.df_freq_frases_ult_salida.index

        # cargo indices de las oraciones de referencia
        ind = list(self.df_freq_frases_ult_salida.indice_sentence)
        
        frases_iguales = []
        indices_frases_iguales = []
        umbral = 0.9
        for p in self.paraphrases:
            score, s1, s2 = p
            if( score > umbral ):
                if ( s1 in ind and s2 in ind ):
                    frases_iguales.append(p)
                    indices_frases_iguales.append(s2)

        # genero salida
        out = self.df_freq_frases_ult_salida[~self.df_freq_frases_ult_salida.indice_sentence.isin(indices_frases_iguales)]

        return list(out['frase_salida'].drop_duplicates()[:15]) # elimino duplicado por las dudas pero no deberian aparecer

    def save(self, filename=DEFAULT_FILENAME):
        """
        graba objeto

        :param filename: ruta+nombre de archivo de salida, defaults to DEFAULT_FILENAME
        :type filename: str
        """
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename=DEFAULT_FILENAME):
        """
        carga de objeto

        :param filename: ruta+nombre de archivo para cargar objeto, defaults to DEFAULT_FILENAME
        :type filename: str
        :return: objeto cargado
        :rtype: clase Autocompleter
        """
        with open(filename, "rb") as f:
            return pickle.load(f)
