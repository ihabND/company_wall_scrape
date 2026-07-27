from funkcije import get_company_data, get_company_links, save_files

firme_linkovi = get_company_links()

firme_lista = []
brojac = 0

for link in firme_linkovi:
    firma = get_company_data(link)
    firme_lista.append(firma)
    # if brojac == 0:
    #     break
    brojac += 1
    print(brojac)

save_files(firme_lista)
print(f"Finished! Scraped {brojac} firms.")