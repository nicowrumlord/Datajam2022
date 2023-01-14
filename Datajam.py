#%%importar librerias
import requests as re
import pandas as pd 
import gradio as gr
#%%obtener datos de la API
limit=110000
def get_data(limit):   #obtiene la data con el numero especificado de resultados variable limit 
    url = f"https://postdata.gov.co/api/action/datastore/search.json?resource_id=1895fbee-42f5-41b5-bba7-a2d03cb0f723&limit={limit}"
    req = re.get(url) #obtiene informacion de la api
    data = req.json()#recupera el json de la api
    result_list = data["result"]["records"] #obtiene los records solicitados y elimina la informacion del principio
    df=pd.DataFrame(result_list)#convierte en data frame de pandas los datos solicitados
    return df,result_list#retorna el data frame
datos,result_list=get_data(limit)#crea un data frame con los datos de la api
#%%pre-procesamiento
datos = datos.astype({"id_empresa":"int32","anno":"int32","trimestre":"int32","trimestre":"int32"})#convierte los datos necesario en tipo entero
#%%funciones 
#%%Funcion busqueda avanzada
def busqueda_avanzada(empresa=None, id_empresa=None, tipo_operador=None, anno=None, trimestre=None,
                      fecha=None, hora_inicio=None,duracion=None, programa=None, 
                      clasificacion=None, genero=None, tipo=None, closed_caption=None, lengua_senas=None, 
                      subtitulado=None, lenguas_nativas=None,limit_data=None):#Se crea la funcion con pametros todos los criterios de busqueda que se quieren
    df=datos#se copia el df original para modificarlo dentro de la funcion
    dicc={}#diccionario para guardar las inputs del usuario
    if empresa:#si exite un campo para x parametro se guarda en el diccionario el valor que en este caso sera lo que ponga el usuario.
        dicc["empresa"]=empresa.upper()#se pone upper porque en los datos todo esta en mayuscula y esto permitira mas flexibilidad
    if id_empresa:
        dicc["id_empresa"]=id_empresa
    if tipo_operador:
        dicc["tipo_operador"]=tipo_operador.upper()
    if anno:
        dicc["anno"]=anno
    if trimestre:
        dicc["trimestre"]=trimestre
    if fecha:
        dicc["fecha"]=fecha
    if hora_inicio:
        dicc["hora_inicio"]=hora_inicio
    if duracion:
        dicc["duracion"]=duracion
    if programa:
        dicc["programa"]=programa.upper()
    if clasificacion:
        dicc["clasificacion"]=clasificacion.upper()
    if genero:
        dicc["genero"]=genero.upper()
    if tipo:
        dicc["tipo"]=tipo.upper()
    if closed_caption:
        dicc["closed_caption"]=closed_caption.upper()
    if lengua_senas:
        dicc["lengua_senas"]=lengua_senas.upper()
    if subtitulado:
        dicc["subtitulado"]=subtitulado.upper()
    if lenguas_nativas:
        dicc["lenguas_nativas"]=lenguas_nativas.upper()
    for x,y in dicc.items():#filtra los datos del data frame teniendo en ceunta cada uno de los parametros dados
        df=df[df[x]==y]     
    df=df.iloc[:,[5,6,8,9,10,11,12]]#Selecciona los datos de interes para el ussuario
    if limit_data:#condicional que permitira limitar los datos al numero deseado
        if limit_data>len(df.index):#elimina errores si se el limit data es mayor al tamaño del df generado con los filtros
            return df.loc[0:len(df.index)]#devuelve el data frame limitado
        else:
            return df.loc[0:limit_data]
    else: 
        return df

#%%busqueda por nombre
def search_by_name(user_in, limite=None):
    limite = int(limite)
    user_in = user_in.upper()
    Name = datos["programa"] == user_in
    df_result = datos[Name]
    if limite:
        if limite > len(df_result):
            return df_result[0:len(df_result.index)]
        else:
            return df_result[0:limite]
    else:
        return df_result.loc[0:1000]

#%%Busqueda general
def busqueda_clasificacion(clasif, limite=None): # retorna un dataframe segun la clasificacion del programa 
    limite = int(limite)
    Religioso = []
    Testimonial = []
    Noticias = []
    Musica = []
    Pelis = []
    Kids = []
    learn =[]
    for dict in result_list:
        for val in dict.values():
            if "EDUCATIVO" in dict.values():
                learn.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])        
            if "MUSICAL" in dict.values():
                Musica.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])
            if "PREDICACIÓN" or "TESTIMONIAL" or "NOTICIERO" in dict.values():
                Religioso.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])
            if "TESTIMONIAL" in  dict.values():
                Testimonial.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])
            if "NOTICIERO" in dict.values():
                Noticias.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])
            if "PELÍCULA" in dict.values():
                Pelis.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])
            if "INFANTIL" in dict.values():
                Kids.append([dict["fecha"], dict["duracion"], dict["programa"], dict['clasificacion'], dict["genero"], dict["tipo_operador"]])

    S_Religioso = set(tuple(i) for i in Religioso)
    S_Test = set(tuple(i) for i in Testimonial)
    S_Noticias = set(tuple(i) for i in Noticias)
    S_Musica = set(tuple(i) for i in Musica)
    S_Pelis = set(tuple(i) for i in Pelis)
    S_Kids = set(tuple(i) for i in Kids)
    S_Learn = set(tuple(i) for i in learn)

    df_Religioso = pd.DataFrame(S_Religioso)
    df_Test = pd.DataFrame(S_Test)
    df_Noticias = pd.DataFrame(S_Noticias)
    df_Musica = pd.DataFrame(S_Musica)
    df_Pelis = pd.DataFrame(S_Pelis)
    df_kids = pd.DataFrame(S_Kids) 
    df_Learn = pd.DataFrame(S_Learn)

    if clasif == "Religioso":
        if limite:
            if limite > len(df_Religioso):
                return df_Religioso[0:len(df_Religioso.index)]
            else:
                return df_Religioso[0:limite]
        else:
            return df_Religioso.loc[0:800]
    elif clasif == "Testimonial":
        if limite:
            if limite > len(df_Test):
                return df_Test.loc[0:len(df_Religioso.index)]
            else: 
                return df_Test.loc[0: limite]
        else:
            return df_Test.loc[0:800]
    elif clasif == "Noticias":
        if limite:
            if limite > len(df_Noticias):
                return df_Noticias.loc[0: len(df_Noticias)]
            else:
                return df_Noticias[0: limite]
        else:
            return df_Noticias.loc[0:800] 
    elif clasif == "Musica":
        if limite:
            if limite > len(df_Musica):
                return df_Musica.loc[0: len(df_Musica)]
            else:
                return df_Musica.loc[0: limite]
        else:
            return df_Musica.loc[0:800] 
    elif clasif == "Pelis":
        if limite:
            if limite > len(df_Pelis):
                return df_kids.loc[0: len(df_Pelis)]
            else:    
                return df_Pelis.loc[0: limite]
        else:
            return df_Pelis.loc[0:800]
    elif clasif == "Kids":
        if limite: 
            if limite > len(df_kids):
                return df_kids.loc[0: len(df_Pelis)]
            else:
                return df_kids.loc[0: limite]
        else:
            return df_kids.loc[0:800]
    elif clasif == "Educativo":
        if limite:
            if limite > len(df_Learn):
                return df_Learn.loc[0: len(df_Learn)]
            else:
                return df_Learn.loc[0: limite]
        else:
            return df_Learn.loc[0:800]

#%% interfaz
interfaz=gr.Blocks(title="seeker", theme="Black")
with interfaz:
    gr.Markdown("SEEKR")
    gr.Markdown("busqueda por nombre o por cualquier parametro en busqueda avanzada, si no sabes que ver revisa busqueda general")
    with gr.Tabs():
        with gr.TabItem("Busqueda por nombre"):
            Limite = gr.Number(label="Limitar el numero de datos que se quiere. Borra el 0 para quitar este parametro de la busqueda")
            entrada=gr.Textbox(label="Nombre del programa")
            salida=gr.DataFrame()
            boton_buscar=gr.Button("Buscar")
        with gr.TabItem("busqueda avanzada"):
            in_empresa=gr.Textbox(label="empresa")
            in_IDempresa=gr.Number(label="ID empresa. Borra el 0 para quitar este parametro de la busqueda")
            in_tipooperador=gr.Textbox(label="tipo operador")
            in_anno=gr.Number(label="Año. Borra el 0 para quitar este parametro de la busqueda")
            in_trimestre=gr.Number(label="Trimestre. Borra el 0 para quitar este parametro de la busqueda")
            in_fecha=gr.Textbox(label="Fecha. ejemplo: 2020-04-01")
            in_horainicio=gr.Textbox(label="Hora De Inicio. ejemplo: 12:59:59")
            in_duracion=gr.Textbox(label="Duracion. ejemplo: 00:28:55")
            in_programa=gr.Textbox(label="programa")
            in_clasificacion=gr.Radio(["FAMILIAR","INFANTIL","ADOLESCENTE","ND","ADULTO"],label="Clasificacion")
            in_genero=gr.Radio(["NO FICCIÓN","FICCIÓN","INFANTIL","INFORMATIVO","ND"],label="Genero")
            in_tipo=gr.Textbox(label="Tipo")
            in_closedcaption=gr.Radio(["NINGUNO","ND","TRANSCRIPCIÓN MANUAL","TRANSCRIPCIÓN AUTOMÁTICA"],label="closed caption")
            in_lenguasenas=gr.Radio(["SI","NO"],label="Lenguaje de señas")
            in_subtitulado=gr.Radio(["SI","NO"],label="Subtitulado")
            in_lenguasnativas=gr.Radio(["SI","NO"],label="Lenguas nativas")
            in_limitdata=gr.Number(label="Limitar el numero de datos que se quiere. Borra el 0 para quitar este parametro de la busqueda")
            inputs_ba=[in_empresa,in_IDempresa,in_tipooperador,in_anno,in_trimestre,in_fecha,
                    in_horainicio,in_duracion,in_programa,in_clasificacion,in_genero,in_tipo,
                    in_closedcaption,in_lenguasenas,in_subtitulado,in_lenguasnativas,in_limitdata]
            salida_ba=gr.DataFrame()
            boton_busquedavanzada=gr.Button("Buscar")
        with gr.TabItem("Busqueda general"):
            limit = gr.Number(label="Limitar el numero de datos que se quiere. Borra el 0 para quitar este parametro de la busqueda")
            entrada_general=gr.Radio(["Noticias", "Religioso", "Pelis", "Testimonial", "Musica", "Kids", "Educativo"], label="Categorias")
            salida_general=gr.DataFrame()
            boton_busquedageneral=gr.Button("Buscar")
    boton_buscar.click(search_by_name, inputs=[entrada, Limite], outputs=salida)
    boton_busquedavanzada.click(busqueda_avanzada, inputs_ba,salida_ba)
    boton_busquedageneral.click(busqueda_clasificacion, inputs=[entrada_general, limit],outputs=salida_general)
    
interfaz.launch(share=True)