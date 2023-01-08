import pandas as pd
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import sys




def  checa_pagina(num_pagina):
    '''
    Checa se existem dados disponíveis para extração na url do site HRC 
    
    uso:
        Passe o parâmetro 'num_pagina' com um número inteiro positivo .
    
    retorno:
        A função retorna os resultados como True/False
        
        True : Encontramos dados nessa página indicada
        False : Não existem dados nessa página indicada
    
    '''
    
    from bs4 import BeautifulSoup
    import requests
    
    req = requests.get(f'https://www.hrc.org/resources/employers/search/p{num_pagina}?q&sort=alpha')

    soup = BeautifulSoup(req.text,'html.parser')
    
    try:
        soup.find('h2',attrs={'class':'heading-24 mb-16'}).text.strip()
        return False
    except:
        return True



def  extract_dados_iniciais(num_pagina):
    '''
    Extrai os dados iniciais das empresas de uma página do site HRC
    
    uso:
        Passe o parâmetro 'num_pagina' com um número inteiro positivo .
    
    retorno:
        A função retorna um DataFrame Pandas com os dados iniciais de todas empresas contidos em uma página do site HRC.
        
        Nome > Nome da Empresa
        Endereço > Endereço da Empresa
        Tipo > Tipo da Empresa ( Corporation,Healthcare Provider, ...)
        URL > URL com dados detalhados da empresa, dentro do HRC
    
    '''
    
    from bs4 import BeautifulSoup
    import requests
    
    try:
        df_empresa = pd.DataFrame()
        dados_empresa = {}

        req = requests.get(f'https://www.hrc.org/resources/employers/search/p{num_pagina}?q')

        soup = BeautifulSoup(req.text, 'html.parser')
        painel = soup.findAll('div',attrs={'class':'wrapper -padded -lg'})[2]
        artigos = painel.findAll('article')

        for item in artigos:

            dados_empresa['nome'] = item.get('aria-label')

            dados_empresa['endereco'] = item.find(class_='flex flex-wrap').find_previous_sibling().text

            dados_empresa['tipo'] = item.find(class_='inline-flex items-center py-16 type-italic text-blue-400 md:self-end').find_previous_sibling().find('p').text


            dados_empresa['URL'] = item.find(class_='block text-current').get('href')

            df_empresa = pd.concat([df_empresa,pd.DataFrame([dados_empresa])], ignore_index=True)

        return df_empresa
    except:
        return f"Erro ao Extrair página > {num_pagina}"
        
        
        
        
def extracao_completa_empresa(url):
    '''
    Extrai os dados completos das empresas de uma página do site HRC
    
    uso:
        Passe o parâmetro 'url' indicando a url específica da empresa dentro do site HRC , ex: https://www.hrc.org/resources/buyers-guide/zoom-video-communications-inc.
    
    retorno:
        A função retorna um DataFrame Pandas com os dados específicos da empresa.

        Company Name
        Company Headquartes
        Company Address
        Company Brands
        Company URL
        Company Score
        criteria_x
        criteria_points_x
        criteria_number_x
        sub_crit_x_x
        detailed_rating_x_x
        criteria_number_x_x
    
        O número de colunas varia dependendo da quantidade de critérios que a empresa possui.
    
    '''
    

    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
        
    
    req = requests.get(url)
    
    soup = BeautifulSoup(req.text,'html.parser')
    
    nome_empresa = soup.find('h1',attrs={'class':'heading-60 mb-32 relative z-1'}).text.strip()
    
    try:
        score = soup.find(class_='bg-yellow-500 heading-48 p-16 text-black text-center w-full md:p-32').text.strip().split('\n')[0]
    except:
        score = ''
        
        
    headquarters = soup.find(string='Headquarters').find_next().text.strip()
    
    address = ' '.join(soup.find(string='Address').find_next().text.split('Map')[0].strip().replace('\n','').split())
    
    try:
        marcas = []
        for i in soup.find(string='Brands').find_next().findAll('span'):
            marcas.append(i.text.strip())
    except:
        marcas = ''
        
    url = soup.find(string='Contact').find_next('a').get('href')
    
    
    df_inicial = pd.DataFrame([[nome_empresa,headquarters,address,marcas,url,score]])
    
    df_inicial = df_inicial.rename(columns={0:'Company Name',1:'Company Headquartes',2:'Company Address',3:'Company Brands',4:'Company URL',5:'Company Score'})
    
    
    layout = soup.findAll(class_='wrapper -padded -lg')[2]
    
    
    criteria_dict = {}
    criteria_df = pd.DataFrame()
    num = 1
    for i in layout.findAll(class_='bg-blue-100 p-24 lg:p-32'):

        criteria_dict['criteria_{}'.format(num)] = i.find('h2',attrs={'class':'heading-32'}).text.strip()

        criteria_dict['criteria_points_{}'.format(num)] = i.find('div',attrs={'class':'text-right'}).find(class_='heading-32').text.strip()

        criteria_dict['criteria_number_{}'.format(num)] = num
        
        criteria_df = pd.concat([criteria_df,pd.DataFrame([criteria_dict])], ignore_index=True)
        

        num+=1
    
    
   
    num = 1
    subcriteria_dict = {}

    subcriteria_df = pd.DataFrame()
    for i in layout.findAll(class_='bg-white p-24 lg:p-32'):
        
        num_in = 1
        for sub in i.findAll(class_='flex leading-tight pr-16 text-14 md:pr-24'):
            
            if sub.find('svg').find('path').get('d') == 'M36.2001 0.400098C16.3001 0.400098 0.200049 16.5001 0.200049 36.4001C0.200049 56.3001 16.3001 72.4001 36.2001 72.4001C56.1001 72.4001 72.2001 56.3001 72.2001 36.4001C72.2001 16.5001 56.1001 0.400098 36.2001 0.400098ZM59.2001 26.9001L33.9001 52.2001C33.2001 52.9001 31.7 53.5001 30.7 53.5001H28.5001C27.5001 53.5001 26 52.9001 25.3 52.2001L13.4001 40.2001C12.7001 39.5001 12.7001 38.3001 13.4001 37.5001L18.1001 32.8001C18.8001 32.1001 20 32.1001 20.8 32.8001L28.4001 40.4001C29.1001 41.1001 30.3001 41.1001 31.0001 40.4001L51.8 19.5001C52.5 18.8001 53.7001 18.8001 54.5001 19.5001L59.2001 24.1001C59.9001 25.0001 59.9001 26.2001 59.2001 26.9001Z':
                detailed_rating = 'Yes'
            elif sub.find('svg').find('path').get('d') == 'M36.2001 0.400098C16.3001 0.400098 0.200049 16.5001 0.200049 36.4001C0.200049 56.3001 16.3001 72.4001 36.2001 72.4001C56.1001 72.4001 72.2001 56.3001 72.2001 36.4001C72.2001 16.5001 56.1001 0.400098 36.2001 0.400098ZM36.2001 63.4001C21.3001 63.4001 9.20005 51.3001 9.20005 36.4001C9.20005 21.5001 21.3001 9.4001 36.2001 9.4001C51.1001 9.4001 63.2001 21.5001 63.2001 36.4001C63.2001 51.3001 51.1001 63.4001 36.2001 63.4001Z':
                detailed_rating = 'No'
            elif sub.find('svg').find('path').get('d') == 'M36.8997 0.700073C16.9997 0.700073 0.899707 16.8001 0.899707 36.7001C0.899707 56.6001 16.9997 72.7001 36.8997 72.7001C56.7997 72.7001 72.8997 56.6001 72.8997 36.7001C72.8997 16.9001 56.7997 0.700073 36.8997 0.700073ZM6.89971 36.7001C6.89971 20.2001 20.3997 6.70007 36.8997 6.70007V66.7001C20.2997 66.7001 6.89971 53.3001 6.89971 36.7001Z':
                detailed_rating = 'Partial'
            elif sub.find('svg').find('path').get('d') == 'M36.2001 0.400098C16.3001 0.400098 0.200049 16.5001 0.200049 36.4001C0.200049 56.3001 16.3001 72.4001 36.2001 72.4001C56.1001 72.4001 72.2001 56.3001 72.2001 36.4001C72.2001 16.5001 56.1001 0.400098 36.2001 0.400098ZM38.6001 57.9001C37.5001 58.9001 36.1001 59.4001 34.4001 59.4001C32.8001 59.4001 31.4001 58.9001 30.4001 57.9001C29.3001 56.9001 28.8 55.5001 28.8 53.9001C28.8 52.3001 29.3001 50.9001 30.4001 49.9001C31.5001 48.9001 32.9001 48.4001 34.5001 48.4001C36.2001 48.4001 37.6001 48.9001 38.7001 49.9001C39.8 50.9001 40.3 52.3001 40.3 53.9001C40.2 55.5001 39.7001 56.9001 38.6001 57.9001ZM48.2001 30.4001C47.6001 31.8001 46.9001 33.0001 46.1001 34.0001C45.3001 35.0001 44.4001 35.8001 43.4001 36.6001C42.5001 37.3001 41.7001 38.0001 40.9001 38.7001C40.2001 39.4001 39.6001 40.3001 39.1001 41.3001C38.6001 42.2001 38.4001 43.3001 38.4001 44.9001V45.9001H30.9001H30.0001L29.9001 45.0001C29.8001 44.3001 29.8 43.6001 29.8 43.0001C29.8 41.7001 29.9 40.5001 30.2 39.5001C30.6 38.0001 31.2001 36.7001 31.9001 35.5001C32.6001 34.4001 33.5001 33.4001 34.4001 32.6001C35.3001 31.8001 36.1 31.1001 36.8 30.4001C37.5 29.7001 38.1001 29.1001 38.6001 28.4001C39.0001 27.8001 39.2001 27.1001 39.2001 26.2001C39.2001 25.0001 38.9 24.2001 38.3 23.6001C37.9 23.1001 36.8001 22.7001 35.0001 22.7001C34.4001 22.7001 33.8 22.8001 33.2001 22.9001C32.5 23.0001 31.9 23.2001 31.2 23.4001C30.5 23.6001 29.9 23.9001 29.3 24.2001C28.7 24.5001 28.1 24.8001 27.7 25.2001L26.8 25.8001L22.9001 18.4001L23.6001 17.9001C25.2001 16.8001 27.0001 15.9001 29.0001 15.3001C31.1001 14.6001 33.5 14.3001 36.3 14.3001C40.1 14.3001 43.3001 15.2001 45.6001 17.2001C47.9001 19.2001 49.1001 21.9001 49.1001 25.1001C49.1001 27.1001 48.8 28.9001 48.2001 30.4001Z':
                detailed_rating = 'No Data'
            elif sub.find('svg').find('path').get('d') == 'M36.2003 0.400098C16.3003 0.400098 0.200293 16.5001 0.200293 36.4001C0.200293 56.3001 16.3003 72.4001 36.2003 72.4001C56.1003 72.4001 72.2003 56.3001 72.2003 36.4001C72.2003 16.5001 56.1003 0.400098 36.2003 0.400098ZM63.2003 36.4001C63.2003 42.2001 61.3003 47.6001 58.2003 52.0001L20.6002 14.4001C25.0002 11.3001 30.4003 9.4001 36.2003 9.4001C51.1003 9.4001 63.2003 21.5001 63.2003 36.4001ZM9.20029 36.4001C9.20029 30.5001 11.1001 25.1001 14.3001 20.7001L51.9002 58.3001C47.5002 61.5001 42.0003 63.4001 36.2003 63.4001C21.3003 63.4001 9.20029 51.3001 9.20029 36.4001Z':
                detailed_rating = 'Not Applicable'

            sub_crit = sub.text.strip().split(':')[1].strip()

            subcriteria_dict['sub_crit_{}_{}'.format(num,num_in)] = sub_crit

            subcriteria_dict['detailed_rating_{}_{}'.format(num,num_in)] = detailed_rating

            subcriteria_dict['criteria_number_{}_{}'.format(num,num_in)] = num

            subcriteria_df = pd.concat([subcriteria_df,pd.DataFrame([subcriteria_dict])], ignore_index=True)
            
            num_in+=1
            
        num+=1

        
    subcriteria_df = subcriteria_df.tail(1)
    criteria_df = criteria_df.tail(1)
    
    lista2 =subcriteria_df.columns.tolist()
    
    lista1 =criteria_df.columns.tolist()
    
    cols = [x for x in lista2 if x not in lista1]
    
    subcriteria_df = subcriteria_df.reset_index(drop=True)
    
    criteria_df = criteria_df.reset_index(drop=True)
    
    
    subcriteria_df = subcriteria_df[cols]

    try:
        part1 = pd.merge(criteria_df,subcriteria_df,how='left', left_index=True,right_index=True)
        return pd.merge(df_inicial,part1,how='cross')
    
    except Exception as E:
        print(E)
        
        return pd.merge(df_inicial,criteria_df,how='cross')
    
   
    
    
    

def main():
    
    
    #url inicial
    url = 'https://www.hrc.org/resources/employers/search?q='

    req = requests.get(url)


    if req.status_code != 200:
        print("Erro ao acessar url")
        sys.exit(1)

  
    # Ao acessar a listagem de empresas, podemos perceber que o site permite que a gente altere a URL e veja os resultados a partir do parametro p <numero da página> , fazendo com que nosso trabalho fique muito mais fácil
   
    #lógica para descobrir quantidade total de páginas a serem capturadas

    num_pagina = 395


    while True:

        check = checa_pagina(num_pagina)
        
        num_pagina+=1
        
        print(check , num_pagina)
        
        if check == False:
            num_max_pagina = num_pagina -1
            print('Não tem dados', check , num_pagina)
            break




    # temos mais de 400 páginas para extrair, portanto, vamos paralelizar a extração dos dados iniciais.

    # ATENÇÃO , use o parâmetro max_workers com MUITA cautela. Isso pode ser prejudicial para o Servidor (Site que estamos extraindo) e para o seu próprio Host (uso massivo de hardware)

    df_init = pd.DataFrame()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_url= (executor.submit(extract_dados_iniciais,pagina) for pagina in range(1,num_max_pagina))

        for cont,future in enumerate(concurrent.futures.as_completed(future_to_url)):
        
            df_in = pd.DataFrame(future.result())

            df_init = pd.concat([df_in, df_init],ignore_index=True)


            print("Extraindo dados iniciais  > ",cont+1,"de ",num_max_pagina)




    #vamos armazenar os dados iniciais
    
    df_init.to_parquet("df_inicial")


    #Separando todas urls que iremos extrair
    urls_empresas = df_init['URL'].unique().tolist()
    
   
   
   
   # temos mais de 4000 empresas para extrair, portanto, vamos paralelizar a extração dos dados iniciais.

    # ATENÇÃO , use o parâmetro max_workers com MUITA cautela. Isso pode ser prejudicial para o Servidor (Site que estamos extraindo) e para o seu próprio Host (uso massivo de hardware)

    df_empresas = pd.DataFrame()

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_to_url= (executor.submit(extracao_completa_empresa,url) for url in urls_empresas)

        for cont,future in enumerate(concurrent.futures.as_completed(future_to_url)):
        
            try:
                df_in = pd.DataFrame(future.result())

                df_empresas = pd.concat([df_in, df_empresas],ignore_index=True)
            except:
                pass


            print("Extraindo empresas  > ",cont+1,"de ",len(urls_empresas))



     #vamos armazenar os dados completos
    
    df_empresas.to_csv("dados_empresas_hrc.csv",sep=';',index=False)




if __name__ == '__main__':

    main()
