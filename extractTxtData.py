class Data():
    def getFirmenname(self, compData) -> str:
        return compData.split('\n')[1]

    def getStraße_n_number(self, compData) -> tuple[str, str]:
        data = compData.split("\n")[2]
        data = data.split(',')

        street_n_number = data[0].split(' ')
        
        street = street_n_number[0:-1]
        street = " ".join(street).strip()
        number = street_n_number[-1].strip()

        return (street, number)

    def getVorwahl_n_nummer(self, compData) -> tuple[str, str]:
        data = compData.split("\n")

        number = data[3]
        number = number.split(' ')
        vorwahl = number[0].strip()
        nummer = number[1].strip()

        return (vorwahl, nummer)

    def getEmail(self, compData) -> str:
        return compData.split("\n")[4].strip()

    def getPw(self, compData) -> str:
        return compData.split("\n")[5].strip()

    def getWebsite(self, compData) -> str:
        return compData.split("\n")[6].strip()

    def getPlz_n_ort(self, compData) -> str:
        data = compData.split("\n")[2]
        data = data.split(',')[1].strip()

        data = data.split(' ')
        plz = data[0]
        ort = data[1]
        
        return (plz, ort)

    def getContentAsList(source : str) -> list:
        with open(source, 'r') as file:
            content = file.read().strip().split("\n\n")

        return content

    def popElementFromFile(self, src : str, elem : str):
        with open(src, 'r') as file:
            content = file.read().strip().split('\n\n')
        
        content.remove(elem)

        with open("remaining_companies.txt", 'w') as file:
            for elem in content:
                file.write(elem + "\n\n")
        
        with open("finished_companies.txt", 'a') as file:
            file.write(f"Email: {self.getEmail(elem)}\n")
            file.write(f"Pw: {self.getPw(elem)}\n")
            file.write("\n")
        

def main():
    crawler = Data().loopTxt(".txt")
    

if __name__ == "__main__":
    main()