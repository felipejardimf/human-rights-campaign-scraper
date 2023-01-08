# human-rights-campaign-scraper
 
![logo](images/logo.png)



Extração de dados de uma campanha de Diretos Humanos que classifica Empresas dos EUA em diversas categorias.

Aqui temos algumas informações específicas que podemos ver na extração completa.


* Company Name
* Company Headquartes
* Company Address
* Company Brands
* Company URL
* Company Score
* Criteria_1
* Criteria_2
* Criteria_n
* criteria_points_1
* criteria_points_2
* criteria_points_n
* criteria_number_1
* criteria_number_2
* criteria_number_n
* detailed_rating_1_1
* detailed_rating_1_n
* SubCriteria_1_1
* SubCriteria_1_2
* SubCriteria_1_n
* SubCriteria_number_1
* SubCriteria_number_2
* SubCriteria_number_n





### Tecnologias utilizadas



* [![BeautifulSoup][BeautifulSoup]][BeautifulSoup-url]
* [![Pandas][Pandas]][Pandas-url]
* [![Requests][Requests]][Requests-url]


[BeautifulSoup-url]: https://beautiful-soup-4.readthedocs.io/en/latest/
[BeautifulSoup]: images/beautifulsouplogo.png
[Pandas-url]: https://pandas.pydata.org/
[Pandas]: images/pandas_logo.png
[Requests-url]: https://requests.readthedocs.io/en/latest/
[Requests]: images/requests_logo.png


### Pré-requisitos


requirements
  ```
  pip install -r requirements.txt
  ```

### Execução


Para executar o Crawler , execute:

  ```
  python -m extract_hrc_empresas.py
  ```
