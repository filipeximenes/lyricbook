#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests


# In[2]:


url = "https://www.letras.mus.br/adiel-luna/maria-fulo/"
url = "https://www.letras.mus.br/adiel-luna/o-coco-vai-comecar-coco-camara/"
url = "https://www.letras.mus.br/pandeiro-do-mestre/cobra-coral/"


# In[3]:


resp = requests.get(url)


# In[4]:


soup = BeautifulSoup(resp.content)


# In[5]:


article = soup.article


# In[6]:


song_name = article.h1.text.strip()


# In[7]:


artist = article.h2.text.strip()


# In[8]:


lyric_html = article.find_all("div", {"class": "cnt-letra-trad"})[0]


# In[9]:


strophes_html = lyric_html.find_all('p')


# In[10]:


lyric = []


# In[11]:


for strophe in strophes_html:
    verses = strophe.get_text(separator='|||').split('|||')
    lyric.append(verses)


# In[12]:


print(song_name)
print(artist)
print(lyric)

