def related_words_extractor(self):
        RW = {}
        found_first_h2 = False
        content_div = self.soup.find('div', id="bodyContent")
        if not content_div:
            content_div = self.soup
            
        
        for e in content_div.find_all(['h2','p'], recursive=True):
            if e.name == 'h2':
                found_first_h2 = True
            if (found_first_h2 == True):
                    # Antes del primer <h2>, solo extraer <p>
                if e.name == 'p':
                    a = e.find_all('a')
                    if a:
                        for i in a:
                            word = i.get_text().strip()
                            href = i.get('href')
                            if word and href:
                                RW[word] = href
            else:
                # Después del primer <h2>, extraer de forma habitual
                if e.name == 'p':
                    a = e.find_all('a')
                    if a:
                        for i in a:
                            word = i.get_text().strip()
                            href = i.get('href')
                            if word and href:
                                RW[word] = href
            
    
            return RW
    