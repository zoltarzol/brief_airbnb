from django.shortcuts import render
import pandas as pd
import re
import functions

# Create your views here.

def country_details_view(request):
    df_air_bnb_anvers = pd.read_csv("data/Antwerp/data/listings.csv")

    df_air_bnb_anvers = df_air_bnb_anvers.drop(columns=["scrape_id","last_scraped","neighborhood_overview","picture_url"])
    df_preparation = df_air_bnb_anvers[["host_id","neighbourhood_cleansed","number_of_reviews"]]
    df_groupby = df_preparation.groupby(by="neighbourhood_cleansed").apply(lambda s: pd.Series({ 
    "host_id nunique": s["host_id"].nunique(), 
    "number_of_reviews sum": s["number_of_reviews"].sum(),}))
    rep1 = df_groupby.to_html(classes='table table-dark table-striped',justify='center')

    df_correction_host_response_rate = df_air_bnb_anvers.host_response_rate.str.replace('%','')
    df_correction_host_response_rate_modifie= pd.to_numeric(df_correction_host_response_rate)
    df_correction_host_response_rate_modifie = df_correction_host_response_rate_modifie.fillna(df_correction_host_response_rate_modifie.mean())

    df_correction_host_acceptance_rate = df_air_bnb_anvers.host_acceptance_rate.str.replace('%','')
    df_correction_host_acceptance_rate_modifie = pd.to_numeric(df_correction_host_acceptance_rate)
    df_correction_host_acceptance_rate_modifie = df_correction_host_acceptance_rate_modifie.fillna(df_correction_host_acceptance_rate_modifie.mean())
    df_correction_host_acceptance_rate_modifie.mean()

    rep2 = [df_correction_host_response_rate_modifie.mean(),df_correction_host_acceptance_rate_modifie.mean()]
    
    nombre_host_total = df_air_bnb_anvers.host_verifications.count()
    nombre_host_email = df_air_bnb_anvers.host_verifications.str.contains('email', regex=False).sum()
    nombre_host_phone = df_air_bnb_anvers.host_verifications.str.contains('phone', regex=False).sum()
    nombre_host_work_email=df_air_bnb_anvers.host_verifications.str.contains('work_email', regex=False).sum()
    rep3 = [(nombre_host_email/nombre_host_total)*100,
        (nombre_host_email/nombre_host_total)*100,
        (nombre_host_email/nombre_host_total)*100]
    
    df_preparation =df_air_bnb_anvers[["room_type","amenities"] ]
    df_preparation["amenities"]=df_preparation.amenities.str.count(",")+1

    df_preparation = df_preparation[["room_type","amenities"] ]
    df_reponse4 = df_preparation.groupby(by="room_type").apply(lambda s: pd.Series({ 
    "amenities mean": s["amenities"].mean(),
     "amenities std": s["amenities"].std()}))
    rep4 = df_reponse4.to_html(classes='table table-dark table-striped',justify='center')

    df_final= df_air_bnb_anvers
    df_final["price"]=pd.to_numeric(df_final["price"].str.replace('$','').str.replace(',',''))
    df_final["price"]
    rep5 = df_final.groupby(by="room_type").apply(lambda s: pd.Series({ 
    "price median": s["price"].median(),
    "price max": s["price"].max(),
    "price min": s["price"].min(),
    "price first_quartile": s["price"].quantile(0.25),
    "price third_quartile": s["price"].quantile(0.75)})).to_html(classes='table table-dark table-striped',justify='center')
    
    df_annonce = df_air_bnb_anvers.bathrooms_text
    df_annonce = df_annonce.apply(lambda s: pd.Series({ 
    "nombres_de_baignoires": functions.first(s),
    "caracteristiques" : functions.last(s)}))

    df_annonce_modifie =df_annonce.caracteristiques.str.replace('private bath','2').str.replace('private baths','2').str.replace('Private half',"1").str.replace('shared bath','0.5').str.replace('shared baths','0.5').str.replace('Half-bath','0.5').str.replace("Shared half","0.25").str.replace('bath','1').str.replace('baths','1').str.replace('s','').str.replace('-1',"")
    df_annonce_modifie = df_annonce_modifie.astype(float)
    df_annonce_finale = pd.DataFrame(df_annonce,columns=["nombres_de_baignoires"])
    df_annonce_finale["caracteristique_nombre"]=df_annonce_modifie
    df_baignoire = pd.DataFrame([x for x in df_annonce_finale["nombres_de_baignoires"]],columns=["nombre_de_baignoire"])
    df_annonce_finale["nombres_de_baignoires"]=df_baignoire["nombre_de_baignoire"].astype(float)
    df_annonce_finale =[x*y for x,y in zip(df_annonce_finale.nombres_de_baignoires , df_annonce_finale.caracteristique_nombre) ] 
    df_annonce_finale = pd.DataFrame(df_annonce_finale,columns=["valeur_baignoire"])
    rep6 = df_annonce_finale.to_html(classes='table table-dark table-striped',justify='center')

    df_description = df_air_bnb_anvers["description"].str.len()
    #Je change la description en nombre de caractères
    df_description= pd.DataFrame(df_description,columns=["description"])
    df_description["number_of_reviews"]=df_air_bnb_anvers["number_of_reviews"]
    #Je transforme df_description en dataframe et je rajoute le nombre de review
    rep7 = df_description.corr().to_html(classes='table table-dark table-striped',justify='center')

    df_air_bnb_anvers_verification = pd.read_csv("data/Antwerp/data/reviews.csv")
    df_listing_reviews = df_air_bnb_anvers.merge(df_air_bnb_anvers_verification, left_on='id', right_on='listing_id') 
    mask =df_listing_reviews['host_name']==df_listing_reviews['reviewer_name']
    nb_equal = df_listing_reviews[mask].shape[0] 

    rep8 = nb_equal/df_listing_reviews.shape[0]*100

    context = {
        'rep1' : rep1,
        'rep2' : rep2,
        'rep3' : rep3,
        'rep4' : rep4,
        'rep5' : rep5,
        'rep6' : rep6,
        'rep7' : rep7,
        'rep8' : rep8,
    }

    # import pudb; pu.db()

    return render(request,'country_details/country_details.html', context=context)