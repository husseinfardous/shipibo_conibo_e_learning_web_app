def create_miscellaneous_corpus():
    
    text_reader = open("miscellaneous/Dictionary_Sentences.txt", "r")
    line_reader = text_reader.readlines()

    text_writer = open("miscellaneous/Dictionary_Sentences_Shi_Spa.txt", "w")

    parallel = False
    parallel_sentence = ""

    for line in line_reader:
        
        line = line.replace("\n", "")
        
        for word in line.split(" "):
            
            if "+" in word:
                word = word.replace("+", "")
            
            if "-" in word:
                word = word.replace("-", "")
            
            if "#" in word:
                word = word.replace("#", "")
            
            if "*" in word:
                word = word.replace("*", "")
            
            if "<" in word:
                word = word.replace("<", "")
                parallel = True
            
            if ">" in word:
                
                if ("." or "!" or "?") not in word:
                    word = word + "."
                
                word = word.replace(">", "")
                parallel_sentence = parallel_sentence + word + "\n"
                text_writer.write(parallel_sentence)
                parallel = False
                parallel_sentence = ""
            
            if parallel and word: 
                parallel_sentence = parallel_sentence + word + " "

    text_reader.close()
    text_writer.close()

def create_seperate_shp_es():
    
    shp_writer = open("miscellaneous/Dictionary_Sentences.shi", "w")
    es_writer = open("miscellaneous/Dictionary_Sentences.spa", "w")

    text_reader = open("miscellaneous/Dictionary_Sentences_Shi_Spa.txt")
    line_reader = text_reader.readlines()

    for line in line_reader:
        if "." in line and line.count(".") == 2:
            if line.count("?") == 2:
                line = line.replace("\n", "").split(".")
                shp_writer.write(line[0].strip().lower() + "\n")
                es_writer.write(line[1].strip().lower() + "\n")
            if line.count(".") == 2: 
                line = line.replace("\n", "").split(".")
                shp_writer.write(line[0].strip().lower() + "." + "\n")
                es_writer.write(line[1].strip().lower() + "." + "\n")

    shp_writer.close()
    es_writer.close()

def main():
    create_miscellaneous_corpus()
    create_seperate_shp_es()

if __name__ == "__main__":
    main()