from pyknow import *


def valida_risposte(domanda, risposte_valide):
    valida = False
    risposta = ""
    domanda = "{}? (".format(domanda)
    for i in range(0, len(risposte_valide)):
        domanda += risposte_valide[i]
        if i != len(risposte_valide) - 1:
            domanda += "|"
        else:
            domanda += ")"
    domanda += " : "
    while not valida:
        risposta = input(domanda)
        if len([risposta_valida for risposta_valida in risposte_valide if risposta_valida == risposta]) > 0:
            valida = True
    return risposta

def si_o_no(domanda):
    return valida_risposte(domanda, ["si","no"])

def altre_risposte(domanda, risposte_valide):
    return valida_risposte(domanda , risposte_valide)

def numerico(domanda):
    while True:
        try:
            valore = float(input("{}? : ".format(domanda)))
            if valore > 3200 or valore < 0:
                raise ArithmeticError
        except ValueError:
            print("Devi inserire un valore numerico")
        except ArithmeticError:
            print("Il valore deve essere maggiore di 0 e minore di 3200")
        else:
            break
    return valore

def leggi_da_file(carenza):
    file = open("diagnosi/diagnosi-carenza-{}.txt".format(carenza) , "r")
    return file.read()

def get_nome_elemento(nome):
    if str.lower(nome) == "carenza boro":
        elemento = "boro"
    elif str.lower(nome) == "carenza cloro":
        elemento = "cloro"
    elif str.lower(nome) == "carenza rame":
        elemento = "rame"
    elif str.lower(nome) == "carenza ferro":
        elemento = "ferro"
    elif str.lower(nome) == "carenza manganese":
        elemento = "manganese"
    elif str.lower(nome) == "carenza molibdeno":
        elemento = "molibdeno"
    elif str.lower(nome) == "carenza zinco":
        elemento = "zinco"
    elif str.lower(nome) == "carenza fosforo":
        elemento = "fosforo"
    elif str.lower(nome) == "carenza potassio":
        elemento = "potassio"
    elif str.lower(nome) == "carenza magnesio":
        elemento = "magnesio"
    elif str.lower(nome) == "carenza calcio":
        elemento = "calcio"
    return elemento 

class Diagnosi(Fact):
    pass

class Terapia(Fact):
  pass


class ExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(inizio='si')
        yield(Fact(cura_fosforo = "Fertilizzare con concimi a rapido assorbimento come il P 20%. I risultati si vedono in 4-5 giorni. Altra fonte di fosforo e' il GK Complete Mix."))
        yield(Fact(cura_azoto = "Fertilizzare con concimi a rapido assorbimento,come Cellmax Bio-Grow. I risultati si vedono in 4-5 giorni. Altre fonti di azoto sono il Bio Nova N 27% e il sangue di bue."))
        yield(Fact(cura_potassio = "Fertilizzare con concime a rapido assorbimento come il K 20%. I risultati si vedono in 2-4 giorni. Altre fonti di Potassio sono il GK Complete Mix e il Rhino Skin."))
        yield(Fact(cura_magnesio = "Fertilizzare con concime idrosolubile a rapido assorbimento come il MgO 8%. I risultati si vedono in 2-4 giorni. Altra fonte di Magnesio (con Calcio, Ferro e altri microelementi) è il Cal-Mag Extra."))
        yield(Fact(cura_calcio = "Fertilizzare con concime a rapido assorbimento come il Mono Calcio 15%. Altra fonte di Calcio sono Cal-Mag Extra e Bio Nova Calcio."))
        yield(Fact(cura_ferro = "Abbassare il pH del suolo ed evitare concimi che contengano Zinco o Manganese. Successivamente applicare chelati di Ferro come il FishPlant Iron."))
        yield(Fact(cura_manganese = "Integrare nella fertirrigazione con concimi ricchi di microelementi, come il Revive e Ionic Cal Mag."))
        yield(Fact(cura_boro = "Fertilizzare con concime idrosolubile a rapido assorbimento come il BORFAST. I risultati si vedono in 2-4 giorni."))
        yield(Fact(cura_zolfo = "In caso di fenomeni di carenza e' possibile aggiungere zolfo inorganico con l'aiuto di concime a base di magnesio, come sale inglese (per l'idrocoltura) e kieserite (per terra da vaso)."))
        yield(Fact(cura_rame = "Integrare nella fertirrigazione con concimi ricchi di microelementi, come il BLOK5."))
        yield(Fact(cura_zinco = "Fertilizzare con concime a rapido assorbimento come ACTISEL o BZFAST. I risultati si vedono in 2-4 giorni."))
        yield(Fact(cura_molibdeno = "Fertilizzare con concime a rapido assorbimento come Molybdenum Fast. I risultati si vedono in 2-4 giorni."))
        yield(Fact(cura_cloro = "Non e' possibile fornire una terapia per la carenza di cloro."))

    """
    REGOLE CONDIVISE
    """

    @Rule(Fact(inizio = "si"))
    def regola_1(self):
        print(str.upper("benvenuto in diagnosi cnp"))
        print("Diagnosi_CNP e' un sistema esperto per riconoscere le carenze nutrizionali nelle coltivazioni , e nelle coltivazioni indoor , basandosi in una fase iniziale sui sintomi visivi presenti sulle foglie della pianta , e in una fase successiva sui valori raccolti da tessuto fogliare o dal terreno. ")
        self.declare(Fact(benvenuto = "si"))

    @Rule(Fact(benvenuto="si"))
    def regola_2(self):
        self.declare(Fact(foglie_colpite=altre_risposte(
            "Sono colpite le foglie giovani , o le foglie più vecchie o basali", ["giovani","vecchie","entrambe"])))

    @Rule(OR(
          AND(
              Fact(foglie_colpite="giovani"),
              Fact(morte_tessuti="no"),
              NOT(Fact(clorosi_internervale = W()))
          ),
          AND(
          Fact(foglie_colpite="entrambe"),
          NOT(Fact(clorosi_internervale = W()))
          )
        ))
    def regola_3(self):
        self.declare(Fact(clorosi_internervale=si_o_no(
            "Le foglie presentano segni di clorosi internervale")))

    @Rule(OR(
        AND(
            Fact(foglie_colpite="giovani"),
            Fact(morte_tessuti="no"),
            Fact(clorosi_internervale="si"),
            Fact(venature_distinte="no"),
            NOT(Fact(spot = W()))
          ),
        AND(
            Fact(foglie_colpite="vecchie"),
            Fact(colore_verde_chiaro="si"),
            NOT(Fact(spot = W()))
        ),
        AND(
            Fact(foglie_colpite="entrambe"),
            Fact(clorosi_internervale = "si"),
            NOT(Fact(spot = W()))
        ),
        AND(
            Fact(foglie_colpite="entrambe"),
            Fact(clorosi_internervale = "no"),
            Fact(aree_clorotiche = "si"),
            NOT(Fact(spot = W()))
        )
        ))
    def regola_4(self):
        self.declare(Fact(spot=si_o_no(
            "Sulla foglia sono presenti aree necrotiche (spot)")))

    """
    FINE REGOLE CONDIVISE
    """

    """
    REGOLE FOGLIE GIOVANI
    """

    @Rule(
        AND(
            Fact(foglie_colpite="giovani"),
            NOT(Fact(morte_tessuti = W()))
            )
        )
    def regola_5(self):
        self.declare(Fact(morte_tessuti=si_o_no(
            "I tessuti in accrescimento della pianta stanno morendo")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="si"),
          NOT(Fact(colore_verde_pallido = W()))
          ))
    def regola_6(self):
        self.declare(Fact(colore_verde_pallido=si_o_no(
            "Le foglie apicali hanno acquisito un colore verde pallido alla base")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="si"),
          Fact(colore_verde_pallido="si"),
          NOT(Fact(arricciate = W()))
          ))
    def regola_7(self):
        self.declare(Fact(arricciate=si_o_no(
            "Le foglie apicali sono arricciate")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="si"),
          Fact(colore_verde_pallido="no"),
          NOT(Fact(forma_uncino = W()))
          ))
    def regola_8(self):
        self.declare(Fact(forma_uncino=si_o_no(
            "Le foglie apicali hanno assunto una forma ad uncino verso il basso")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="si"),
          Fact(colore_verde_pallido="no"),
          Fact(forma_uncino="si"),
          NOT(Fact(color_marrone = W()))
          ))
    def regola_9(self):
        self.declare(Fact(color_marrone=si_o_no(
            "Le foglie apicali stanno diventando di color marrone")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          NOT(Fact(verde_chiaro_diffuso = W()))
          ),
          salience=10)
    def regola_11(self):
        self.declare(Fact(verde_chiaro_diffuso=si_o_no(
            "Sulla foglia sono presenti zone di colore verde chiaro")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          Fact(verde_chiaro_diffuso="no"),
          NOT(Fact(clorotiche = W()))
          ))
    def regola_12(self):
        self.declare(Fact(clorotiche=si_o_no(
            "Le foglie sono clorotiche")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          Fact(verde_chiaro_diffuso="no"),
          Fact(clorotiche="si"),
          NOT(Fact(apici_sbiancati = W()))
          ))
    def regola_13(self):
        self.declare(Fact(apici_sbiancati=si_o_no(
            "Gli apici delle foglie sono sbiancati")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="si"),
          NOT(Fact(venature_distinte = W()))
          ))
    def regola_14(self):
        self.declare(Fact(venature_distinte=si_o_no(
            "La foglia presenta una chiara distinzione tra le venature e le aree cloritiche")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          Fact(verde_chiaro_diffuso = "no"),
          Fact(clorotiche = "no"),
          NOT(Fact(clorosi_internervale_mediane = W()))
          ))
    def regola_15(self):
        self.declare(Fact(clorosi_internervale_mediane=si_o_no(
            "Le foglie mediane presentano clorosi internervale")))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          Fact(clorosi_internervale_mediane="si"),
          NOT(Fact(crescita_bloccata = W()))
          ))
    def regola_16(self):
        self.declare(Fact(crescita_bloccata=si_o_no(
            "La crescita delle foglie e' bloccata")))

    """
    REGOLE FOGLIE VECCHIE O BASALI
    """

    @Rule(
        AND(
            Fact(foglie_colpite="vecchie"),
            NOT(Fact(colore_verde_scuro = W()))
            )
        )
    def regola_17(self):
        self.declare(Fact(colore_verde_scuro=si_o_no(
            "Le foglie hanno assunto un colore verde scuro")))

    @Rule(AND(
        Fact(foglie_colpite="vecchie"),
        Fact(colore_verde_scuro="si"),
        NOT(Fact(spot_rossastri = W()))
    ))
    def regola_18(self):
        self.declare(Fact(spot_rossastri=si_o_no(
            "Sono presenti degli spot rossastri sulle foglie")))

    @Rule(AND(
        Fact(foglie_colpite="vecchie"),
        Fact(colore_verde_scuro="no"),
        NOT(Fact(colore_verde_chiaro = W()))
    ))
    def regola_19(self):
        self.declare(Fact(colore_verde_chiaro=si_o_no(
            "Le foglie presentano un colore verde chiaro")))

    @Rule(AND(
        Fact(foglie_colpite="vecchie"),
        Fact(colore_verde_chiaro="si"),
        Fact(spot="si"),
        NOT(Fact(concave_arricciate = W()))
    ))
    def regola_21(self):
        self.declare(Fact(concave_arricciate=si_o_no(
            "Le foglie sono concave e arricciate")))


    """
    FINE REGOLE FOGLIE VECCHIE O BASALI
    """

    """
    REGOLE EFFETTI LOCALIZZATI
    """

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "si"),
        NOT(Fact(foglie_rosse = W()))
        ))
    def regola_22(self):
        self.declare(Fact(foglie_rosse=si_o_no(
            "Sono presenti foglie rosse")))

#Unire con le zone clorotiche dei sintomi foglie giovani
    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "no"),
        NOT(Fact(aree_clorotiche = W()))
        ))
    def regola_23(self):
        self.declare(Fact(aree_clorotiche=si_o_no(
            "Sono presenti aree clorotiche sulle foglie")))

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "no"),
        Fact(aree_clorotiche = "si"),
        Fact(spot = "no"),
        NOT(Fact(bruciature = W()))
        ))
    def regola_24(self):
        self.declare(Fact(bruciature=si_o_no(
            "Le foglie presentano bruciature (anche a macchie) sui margini")))

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "no"),
        Fact(aree_clorotiche = "si"),
        Fact(spot="si"),
        NOT(Fact(separazione_netta = W()))
        ))
    def regola_26(self):
        self.declare(Fact(separazione_netta=si_o_no(
            "La separazione tra tessuti vivi e morti è netta")))


    """
    FINE REGOLE EFFETTI LOCALIZZATI
    """

    """
    REGOLE ANALISI VALORI ESTRATTI DAI TESSUTI FOGLIARI
    """

    @Rule(
        AND(
            Diagnosi(nome = MATCH.nome),
            OR(
                TEST(lambda nome: nome == "Carenza Boro"),
                TEST(lambda nome: nome == "Carenza Cloro"),
                TEST(lambda nome: nome == "Carenza Rame"),
                TEST(lambda nome: nome == "Carenza Ferro"),
                TEST(lambda nome: nome == "Carenza Manganese"),
                TEST(lambda nome: nome == "Carenza Molibdeno"),
                TEST(lambda nome: nome == "Carenza Zinco"),
            ),
            NOT(Fact(campione_tessuti = W())),
        ),
        salience = 3
        )
    def regola_27(self,nome):
        self.declare(Fact(campione_tessuti=si_o_no(
            "Hai a disposizione i valori di {} in ppm recuperati da tessuti fogliari".format(get_nome_elemento(nome)))))

    @Rule(
         AND(
             Diagnosi(nome = MATCH.nome),
             OR(
                TEST(lambda nome: nome == "Carenza Fosforo"),
                TEST(lambda nome: nome == "Carenza Potassio"),
                TEST(lambda nome: nome == "Carenza Magnesio"),
                TEST(lambda nome: nome == "Carenza Calcio"),
                TEST(lambda nome: nome == "Carenza Ferro"),
                TEST(lambda nome: nome == "Carenza Manganese"),
                TEST(lambda nome: nome == "Carenza Zinco"),
                TEST(lambda nome: nome == "Carenza Rame"),
                TEST(lambda nome: nome == "Carenza Boro"),
            ),
            NOT(Fact(campione_terreno = W()))
         ),
         salience = 2
         )
    def regola_28(self,nome):
         self.declare(Fact(campione_terreno=si_o_no(
             "Hai a disposizione i valori di {} in mg/kg recuperati dal terreno".format(get_nome_elemento(nome)))))

    @Rule(
        Diagnosi(nome = "Carenza Boro"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_29(self):
        self.declare(Fact(percentuale_tessuti_boro=numerico(
            "Quant'è la percentuale di Boro")))

    @Rule(
        Diagnosi(nome = "Carenza Cloro"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_30(self):
        self.declare(Fact(percentuale_tessuti_cloro=numerico(
            "Quant'è la percentuale di Cloro")))

    @Rule(
        Diagnosi(nome = "Carenza Rame"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_31(self):
        self.declare(Fact(percentuale_tessuti_rame=numerico(
            "Quant'è la percentuale di Rame")))

    @Rule(
        Diagnosi(nome = "Carenza Ferro"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_32(self):
        self.declare(Fact(percentuale_tessuti_ferro=numerico(
            "Quant'è la percentuale di Ferro")))

    @Rule(
        Diagnosi(nome = "Carenza Manganese"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_33(self):
        self.declare(Fact(percentuale_tessuti_manganese=numerico(
            "Quant'è la percentuale di Manganese")))

    @Rule(
        Diagnosi(nome = "Carenza Molibdeno"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_34(self):
        self.declare(Fact(percentuale_tessuti_molibdeno=numerico(
            "Quant'è la percentuale di Molibdeno")))

    @Rule(
        Diagnosi(nome = "Carenza Zinco"),
        Fact(campione_tessuti = "si"),
        salience = 3
    )
    def regola_35(self):
        self.declare(Fact(percentuale_tessuti_zinco=numerico(
            "Quant'è la percentuale di Zinco")))

    @Rule(
        Diagnosi(nome = "Carenza Fosforo"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_36(self):
        self.declare(Fact(percentuale_terreno_fosforo=numerico(
            "Quant'è la percentuale di Fosforo")))

    @Rule(
        Diagnosi(nome = "Carenza Potassio"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_37(self):
        self.declare(Fact(percentuale_terreno_potassio=numerico(
            "Quant'è la percentuale di Potassio")))

    @Rule(
        Diagnosi(nome = "Carenza Magnesio"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_38(self):
        self.declare(Fact(percentuale_terreno_magnesio=numerico(
            "Quant'è la percentuale di Magnesio")))

    @Rule(
        Diagnosi(nome = "Carenza Calcio"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_39(self):
        self.declare(Fact(percentuale_terreno_calcio=numerico(
            "Quant'è la percentuale di Calcio")))

    @Rule(
        Diagnosi(nome = "Carenza Ferro"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_40(self):
        self.declare(Fact(percentuale_terreno_ferro=numerico(
            "Quant'è la percentuale di Ferro")))

    @Rule(
        Diagnosi(nome = "Carenza Manganese"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_41(self):
        self.declare(Fact(percentuale_terreno_manganese=numerico(
            "Quant'è la percentuale di Manganese")))

    @Rule(
        Diagnosi(nome = "Carenza Zinco"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_42(self):
        self.declare(Fact(percentuale_terreno_zinco=numerico(
            "Quant'è la percentuale di Zinco")))

    @Rule(
        Diagnosi(nome = "Carenza Rame"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_43(self):
        self.declare(Fact(percentuale_terreno_rame=numerico(
            "Quant'è la percentuale di Rame")))

    @Rule(
        Diagnosi(nome = "Carenza Boro"),
        Fact(campione_terreno = "si"),
        salience = 2
    )
    def regola_44(self):
        self.declare(Fact(percentuale_terreno_boro=numerico(
            "Quant'è la percentuale di Boro")))

    """
    FINE REGOLE VALORI ESTRATTI DAI TESSUTI FOGLIARI
    """

    """
    REGOLE CALCOLO % TESSUTI FOGLIARI
    """

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(Fact(percentuale_tessuti_boro=MATCH.percentuale_tessuti_boro)),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) < 5),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_boro_0(self):
        self.declare(Fact(livello_tessuti_fogliari="grave carenza"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_boro=MATCH.percentuale_tessuti_boro),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) >= 5),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) < 30),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_boro_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_boro=MATCH.percentuale_tessuti_boro),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) >= 30),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) < 200),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_boro_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_boro=MATCH.percentuale_tessuti_boro),
        TEST(lambda percentuale_tessuti_boro: float(percentuale_tessuti_boro) >= 200),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_boro_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))


    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_cloro=MATCH.percentuale_tessuti_cloro),
        TEST(lambda percentuale_tessuti_cloro: float(percentuale_tessuti_cloro) < 100),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_cloro_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_cloro=MATCH.percentuale_tessuti_cloro),
        TEST(lambda percentuale_tessuti_cloro: float(percentuale_tessuti_cloro) >= 100),
        TEST(lambda percentuale_tessuti_cloro: float(percentuale_tessuti_cloro) < 500),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_cloro_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_cloro=MATCH.percentuale_tessuti_cloro),
        TEST(lambda percentuale_tessuti_cloro: float(percentuale_tessuti_cloro) >= 500),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_cloro_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_rame=MATCH.percentuale_tessuti_rame),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) < 2),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_rame_0(self):
        self.declare(Fact(livello_tessuti_fogliari="grave carenza"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_rame=MATCH.percentuale_tessuti_rame),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) >= 2),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) < 5),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_rame_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_rame=MATCH.percentuale_tessuti_rame),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) >= 5),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) < 30),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_rame_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_rame=MATCH.percentuale_tessuti_rame),
        TEST(lambda percentuale_tessuti_rame: float(percentuale_tessuti_rame) > 30),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_rame_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_ferro=MATCH.percentuale_tessuti_ferro),
        TEST(lambda percentuale_tessuti_ferro: float(percentuale_tessuti_ferro) < 50),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_ferro_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_ferro=MATCH.percentuale_tessuti_ferro),
        TEST(lambda percentuale_tessuti_ferro: float(percentuale_tessuti_ferro) >= 50),
        TEST(lambda percentuale_tessuti_ferro: float(percentuale_tessuti_ferro) < 500),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_ferro_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_ferro=MATCH.percentuale_tessuti_ferro),
        TEST(lambda percentuale_tessuti_ferro: float(percentuale_tessuti_ferro) >= 500),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_ferro_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_manganese=MATCH.percentuale_tessuti_manganese),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) < 15),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_manganese_0(self):
        self.declare(Fact(livello_tessuti_fogliari="grave carenza"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_manganese=MATCH.percentuale_tessuti_manganese),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) >= 15),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) < 25),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_manganese_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_manganese=MATCH.percentuale_tessuti_manganese),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) >= 25),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) < 300),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_manganese_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_manganese=MATCH.percentuale_tessuti_manganese),
        TEST(lambda percentuale_tessuti_manganese: float(percentuale_tessuti_manganese) > 300),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_manganese_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_molibdeno=MATCH.percentuale_tessuti_molibdeno),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) < 0.03),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_molibdeno_0(self):
        self.declare(Fact(livello_tessuti_fogliari="grave carenza"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_molibdeno=MATCH.percentuale_tessuti_molibdeno),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) >= 0.03),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) < 0.15),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_molibdeno_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_molibdeno=MATCH.percentuale_tessuti_molibdeno),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) >= 0.15),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) < 2),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_molibdeno_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_molibdeno=MATCH.percentuale_tessuti_molibdeno),
        TEST(lambda percentuale_tessuti_molibdeno: float(percentuale_tessuti_molibdeno) >= 2),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_molibdeno_3(self):
        self.declare(Fact(livello_tessuti_fogliari="eccesso"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_zinco=MATCH.percentuale_tessuti_zinco),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) < 10),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_zinco_0(self):
        self.declare(Fact(livello_tessuti_fogliari="grave carenza"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_zinco=MATCH.percentuale_tessuti_zinco),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) >= 10),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) < 20),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_zinco_1(self):
        self.declare(Fact(livello_tessuti_fogliari="livello carente"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_zinco=MATCH.percentuale_tessuti_zinco),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) >= 20),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) < 150),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_zinco_2(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    @Rule(
        Fact(campione_tessuti = "si"),
        Fact(percentuale_tessuti_zinco=MATCH.percentuale_tessuti_zinco),
        TEST(lambda percentuale_tessuti_zinco: float(percentuale_tessuti_zinco) >= 150),
        NOT(Fact(livello_tessuti_fogliari = W())),
        salience = 3
        )
    def tessuto_carenza_zinco_3(self):
        self.declare(Fact(livello_tessuti_fogliari="livello normale"))

    """
    FINE REGOLE CALCOLO % TESSUTI FOGLIARI
    """

    """
    REGOLE CALCOLO % TERRENO
    """

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_fosforo=MATCH.percentuale_terreno_fosforo),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) < 7),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_fosforo_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_fosforo=MATCH.percentuale_terreno_fosforo),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) >= 7),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) < 14),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_fosforo_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_fosforo=MATCH.percentuale_terreno_fosforo),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) >= 14),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) < 20),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_fosforo_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_fosforo=MATCH.percentuale_terreno_fosforo),
        TEST(lambda percentuale_terreno_fosforo: float(percentuale_terreno_fosforo) >= 20),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_fosforo_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_potassio=MATCH.percentuale_terreno_potassio),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) < 40),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_potassio_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_potassio=MATCH.percentuale_terreno_potassio),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) >= 40),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) < 80),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_potassio_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_potassio=MATCH.percentuale_terreno_potassio),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) >= 80),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) < 120),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_potassio_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_potassio=MATCH.percentuale_terreno_potassio),
        TEST(lambda percentuale_terreno_potassio: float(percentuale_terreno_potassio) >= 120),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_potassio_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_magnesio=MATCH.percentuale_terreno_magnesio),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) < 50),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_magnesio_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_magnesio=MATCH.percentuale_terreno_magnesio),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) >= 50),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) < 100),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_magnesio_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_magnesio=MATCH.percentuale_terreno_magnesio),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) >= 100),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) < 150),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_magnesio_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_magnesio=MATCH.percentuale_terreno_magnesio),
        TEST(lambda percentuale_terreno_magnesio: float(percentuale_terreno_magnesio) >= 150),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_magnesio_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_calcio=MATCH.percentuale_terreno_calcio),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) < 1000),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_calcio_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_calcio=MATCH.percentuale_terreno_calcio),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) >= 1000),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) < 2000),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_calcio_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_calcio=MATCH.percentuale_terreno_calcio),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) >= 2000),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) < 3000),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_calcio_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_calcio=MATCH.percentuale_terreno_calcio),
        TEST(lambda percentuale_terreno_calcio: float(percentuale_terreno_calcio) >= 3000),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_calcio_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_ferro=MATCH.percentuale_terreno_ferro),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) < 2.5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_ferro_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_ferro=MATCH.percentuale_terreno_ferro),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) >= 2.5),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) < 5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_ferro_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_ferro=MATCH.percentuale_terreno_ferro),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) >= 5),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) < 10),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_ferro_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_ferro=MATCH.percentuale_terreno_ferro),
        TEST(lambda percentuale_terreno_ferro: float(percentuale_terreno_ferro) >= 10),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_ferro_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_manganese=MATCH.percentuale_terreno_manganese),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) < 2),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_manganese_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_manganese=MATCH.percentuale_terreno_manganese),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) >= 2),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) < 4),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_manganese_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_manganese=MATCH.percentuale_terreno_manganese),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) >= 4),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) < 6),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_manganese_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_manganese=MATCH.percentuale_terreno_manganese),
        TEST(lambda percentuale_terreno_manganese: float(percentuale_terreno_manganese) >= 6),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_manganese_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_zinco=MATCH.percentuale_terreno_zinco),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) < 1),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_zinco_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_zinco=MATCH.percentuale_terreno_zinco),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) >= 1),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) < 3),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_zinco_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_zinco=MATCH.percentuale_terreno_zinco),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) >= 3),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) < 5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_zinco_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_zinco=MATCH.percentuale_terreno_zinco),
        TEST(lambda percentuale_terreno_zinco: float(percentuale_terreno_zinco) >= 5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_zinco_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_rame=MATCH.percentuale_terreno_rame),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) < 1),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_rame_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_rame=MATCH.percentuale_terreno_rame),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) >= 1),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) < 3),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_rame_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_rame=MATCH.percentuale_terreno_rame),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) >= 3),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) < 5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_rame_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_rame=MATCH.percentuale_terreno_rame),
        TEST(lambda percentuale_terreno_rame: float(percentuale_terreno_rame) >= 5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_rame_4(self):
        self.declare(Fact(livello_terreno="eccesso"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_boro=MATCH.percentuale_terreno_boro),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) < 0.1),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_boro_0(self):
        self.declare(Fact(livello_terreno="grave carenza"))
    
    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_boro=MATCH.percentuale_terreno_boro),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) >= 0.1),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) < 0.3),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_boro_1(self):
        self.declare(Fact(livello_terreno="livello carente"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_boro=MATCH.percentuale_terreno_boro),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) >= 0.3),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) < 0.5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_boro_2(self):
        self.declare(Fact(livello_terreno="livello normale"))

    @Rule(
        Fact(campione_terreno = "si"),
        Fact(percentuale_terreno_boro=MATCH.percentuale_terreno_boro),
        TEST(lambda percentuale_terreno_boro: float(percentuale_terreno_boro) >= 0.5),
        NOT(Fact(livello_terreno = W())),
        salience = 2
        )
    def terreno_carenza_boro_4(self):
        self.declare(Fact(livello_terreno="eccesso"))
    
    """
    FINE REGOLE CALCOLO % TERRENO
    """

    """
    DIAGNOSI
    """

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="si"),
                Fact(colore_verde_pallido="si"),
                Fact(arricciate="si"),
                Fact(cura_boro = MATCH.cura_boro)
            )
          )
    def diagnosi_carenza_boro(self, cura_boro):
        self.declare(Diagnosi(
            nome="Carenza Boro",
            descrizione=leggi_da_file("boro")
            ))
        print("E' stata riscontrata una carenza di boro.")
        self.declare(Terapia(nome = "Cura carenza Boro", descrizione = cura_boro))

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="si"),
                Fact(colore_verde_pallido="no"),
                Fact(forma_uncino="si"),
                Fact(color_marrone="si"),
                Fact(cura_calcio = MATCH.cura_calcio)
            )   
          )
    def diagnosi_carenza_calcio(self, cura_calcio):
        self.declare(Diagnosi(
            nome="Carenza Calcio",
            descrizione=leggi_da_file("calcio")
            ))
        print("E' stata riscontrata una carenza di calcio.")
        self.declare(Terapia(nome = "Cura carenza Calcio", descrizione = cura_calcio))

    @Rule(AND(
          Fact(foglie_colpite="giovani"),
          Fact(morte_tessuti="no"),
          Fact(clorosi_internervale="no"),
          Fact(verde_chiaro_diffuso="si"),
          Fact(cura_zolfo = MATCH.cura_zolfo)
          ))
    def diagnosi_carenza_zolfo(self, cura_zolfo):
        self.declare(Diagnosi(
            nome="Carenza Zolfo",
            descrizione=leggi_da_file("zolfo")
            ))
        print("E' stata riscontrata una carenza di zolfo.")
        self.declare(Terapia(nome = "Cura carenza Zolfo", descrizione = cura_zolfo))

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="no"),
                Fact(clorosi_internervale="no"),
                Fact(verde_chiaro_diffuso="no"),
                Fact(clorotiche="si"),
                Fact(apici_sbiancati="si"),
                Fact(cura_rame = MATCH.cura_rame)
            )
        )
    def diagnosi_carenza_rame(self, cura_rame):
        self.declare(Diagnosi(
            nome="Carenza Rame",
            descrizione=leggi_da_file("Rame")
            ))
        print("E' stata riscontrata una carenza di rame.")
        self.declare(Terapia(nome = "Cura carenza Rame", descrizione = cura_rame))

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="no"),
                Fact(clorosi_internervale="si"),
                Fact(venature_distinte="si"),
                Fact(cura_ferro = MATCH.cura_ferro)
            ) 
          )
    def diagnosi_carenza_ferro(self, cura_ferro):
        self.declare(Diagnosi(
            nome="Carenza Ferro",
            descrizione=leggi_da_file("ferro")
            ))
        print("E' stata riscontrata una carenza di ferro.")
        self.declare(Terapia(nome = "Cura carenza Ferro", descrizione = cura_ferro))

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="no"),
                Fact(clorosi_internervale="si"),
                Fact(venature_distinte="no"),
                Fact(spot="si"),
                Fact(cura_manganese = MATCH.cura_manganese)
            )
          )
    def diagnosi_carenza_manganese(self, cura_manganese):
        self.declare(Diagnosi(
            nome="Carenza Manganese",
            descrizione=leggi_da_file("manganese")
            ))
        print("E' stata riscontrata una carenza di manganese.")
        self.declare(Terapia(nome = "Cura carenza Manganese", descrizione = cura_manganese))

    @Rule(
            AND(
                Fact(foglie_colpite="giovani"),
                Fact(morte_tessuti="no"),
                Fact(clorosi_internervale="no"),
                Fact(clorosi_internervale_mediane="si"),
                Fact(crescita_bloccata="si"),
                Fact(cura_zinco = MATCH.cura_zinco)
            )
          )
    def diagnosi_carenza_zinco(self, cura_zinco):
        self.declare(Fact(diagnosi="carenza zinco"))
        self.declare(Diagnosi(
            nome="Carenza Zinco",
            descrizione=leggi_da_file("zinco")
            ))
        print("E' stata riscontrata una carenza di zinco.")
        self.declare(Terapia(nome = "Cura carenza Zinco", descrizione = cura_zinco))

    @Rule(AND(
        Fact(foglie_colpite="vecchie"),
        Fact(colore_verde_scuro="si"),
        Fact(spot_rossastri="si"),
        Fact(cura_fosforo = MATCH.cura_fosforo)
    ))
    def diagnosi_carenza_fosforo(self, cura_fosforo):
        self.declare(Diagnosi(
            nome="Carenza Fosforo",
            descrizione=leggi_da_file("fosforo")
            ))
        print("E' stata riscontrata una carenza di fosforo.")
        self.declare(Terapia(nome = "Cura carenza Fosforo", descrizione = cura_fosforo))

    @Rule(AND(
        Fact(foglie_colpite="vecchie"),
        Fact(colore_verde_chiaro="si"),
        Fact(spot="no"),
        Fact(cura_azoto = MATCH.cura_azoto)
    ))
    def diagnosi_carenza_azoto(self, cura_azoto):
        self.declare(Diagnosi(
            nome="Carenza Azoto",
            descrizione=leggi_da_file("azoto")
            ))
        print("E' stata riscontrata una carenza di azoto.")
        self.declare(Terapia(nome = "Cura carenza Azoto", descrizione = cura_azoto))

    @Rule(
            AND(
                Fact(foglie_colpite="vecchie"),
                Fact(colore_verde_chiaro="si"),
                Fact(spot="si"),
                Fact(concave_arricciate="si"),
                Fact(cura_molibdeno = MATCH.cura_molibdeno)
            )
        )
    def diagnosi_carenza_molibdeno(self, cura_molibdeno):
        self.declare(Diagnosi(
            nome="Carenza Molibdeno",
            descrizione=leggi_da_file("molibdeno")
            ))
        print("E' stata riscontrata una carenza di molibdeno.")
        self.declare(Terapia(nome = "Cura carenza Molibdeno", descrizione = cura_molibdeno))

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale="si"),
        Fact(spot="si"),
        Fact(foglie_rosse="si"),
        Fact(cura_magnesio = MATCH.cura_magnesio)
    ))
    def diagnosi_carenza_magnesio(self, cura_magnesio):
        self.declare(Diagnosi(
            nome="Carenza Magnesio",
            descrizione=leggi_da_file("magnesio")
            ))
        print("E' stata riscontrata una carenza di magnesio.")
        self.declare(Terapia(nome = "Cura carenza Magnesio", descrizione = cura_magnesio))

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "no"),
        Fact(aree_clorotiche = "si"),
        Fact(bruciature="si"),
        Fact(cura_potassio = MATCH.cura_potassio)
        ))
    def diagnosi_carenza_potassio(self, cura_potassio):
        self.declare(Diagnosi(
            nome="Carenza Potassio",
            descrizione=leggi_da_file("potassio")
            ))
        print("E' stata riscontrata una carenza di potassio.")
        self.declare(Terapia(nome = "Cura carenza Potassio", descrizione = cura_potassio))

    @Rule(AND(
        Fact(foglie_colpite="entrambe"),
        Fact(clorosi_internervale = "no"),
        Fact(aree_clorotiche = "si"),
        Fact(spot="si"),
        Fact(separazione_netta="si"),
        Fact(cura_cloro = MATCH.cura_cloro)
        ))
    def diagnosi_carenza_cloro(self, cura_cloro):
        self.declare(Diagnosi(
            nome="Carenza Cloro",
            descrizione=leggi_da_file("cloro")
            ))
        print("E' stata riscontrata una carenza di cloro.")
        self.declare(Terapia(nome = "Cura carenza Cloro", descrizione = cura_cloro))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
            AND(
                OR(
                    Fact(livello_tessuti_fogliari = "grave carenza"),
                    Fact(livello_tessuti_fogliari = "livello carente")
                ),
                OR(
                    Fact(livello_terreno = "grave carenza"),
                    Fact(livello_terreno = "livello carente")
                )
            ),AND(
                OR(
                    Fact(livello_tessuti_fogliari = "livello normale"),
                    Fact(livello_tessuti_fogliari = "eccessivo")
                ),
                OR(
                    Fact(livello_terreno = "grave carenza"),
                    Fact(livello_terreno = "livello carente")
                )
            )
        ), 
        Fact(livello_tessuti_fogliari = MATCH.livello_tessuti_fogliari),
        Fact(livello_terreno = MATCH.livello_terreno),
        salience = 1
    )
    def stampa_diagnosi_1(self, nome, descrizione, livello_tessuti_fogliari, livello_terreno):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del tessuto fogliare"))
        print("L'analisi delle percentuali di {} in ppm nei tessuti fogliari , ha evidenziato un/una  {} dell'elemento.".format(get_nome_elemento(nome) , livello_tessuti_fogliari)) 
        print(str.upper("analisi del terreno"))
        print("L'analisi delle percentuali di {} in mg/kg nel terreno , ha evidenziato un/una  {} dell'elemento nel terreno.".format(get_nome_elemento(nome) , livello_terreno))
        self.declare(Fact(terapia=si_o_no("Vuoi che ti venga proposta una possibile terapia")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
            AND(
                OR(
                    Fact(livello_tessuti_fogliari = "livello normale"),
                    Fact(livello_tessuti_fogliari = "eccesso")
                ),
                OR(
                    Fact(livello_terreno = "livello normale"),
                    Fact(livello_terreno = "eccesso")
                )
            ),
            AND(
                OR(
                    Fact(livello_tessuti_fogliari = "grave carenza"),
                    Fact(livello_tessuti_fogliari = "livello carente")
                ),
                OR(
                    Fact(livello_terreno = "livello normale"),
                    Fact(livello_terreno = "eccesso")
                )
            )
        ),
        Fact(livello_tessuti_fogliari = MATCH.livello_tessuti_fogliari),
        Fact(livello_terreno = MATCH.livello_terreno),
        salience = 1
    )
    def stampa_diagnosi_2(self, nome, descrizione, livello_tessuti_fogliari, livello_terreno):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del tessuto fogliare"))
        print("L'analisi delle percentuali di {} in ppm nei tessuti fogliari , ha evidenziato un/una  {} dell'elemento.".format(get_nome_elemento(nome) , livello_tessuti_fogliari)) 
        print(str.upper("analisi del terreno"))
        print("L'analisi delle percentuali di {} in mg/kg nel terreno , ha evidenziato un/una  {} dell'elemento nel terreno.".format(get_nome_elemento(nome) , livello_terreno))
        print(str.upper("terapia"))
        print("I dati raccolti dal terreno fanno evincere che i livello del nutriente nel terreno, e nei tessuti fogliari sono buoni, quindi il problema può essere dovuto a una malattia della pianta , o a un parassita")
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
                Fact(livello_tessuti_fogliari = "grave carenza"),
                Fact(livello_tessuti_fogliari = "livello carente")
        ),
        NOT(Fact(livello_terreno = W())),
        Fact(livello_tessuti_fogliari = MATCH.livello_tessuti_fogliari),
        salience = 1
    )
    def stampa_diagnosi_3(self, nome, descrizione, livello_tessuti_fogliari):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del tessuto fogliare"))
        print("L'analisi delle percentuali di {} in ppm nei tessuti fogliari , ha evidenziato un/una  {} dell'elemento.".format(get_nome_elemento(nome) , livello_tessuti_fogliari)) 
        self.declare(Fact(terapia=si_o_no("Vuoi che ti venga proposta una possibile terapia")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
                Fact(livello_tessuti_fogliari = "livello normale"),
                Fact(livello_tessuti_fogliari = "eccesso")
        ),
        NOT(Fact(livello_terreno = W())),
        Fact(livello_tessuti_fogliari = MATCH.livello_tessuti_fogliari),
        salience = 1
    )
    def stampa_diagnosi_4(self, nome, descrizione, livello_tessuti_fogliari):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del tessuto fogliare"))
        print("L'analisi delle percentuali di {} in ppm nei tessuti fogliari , ha evidenziato un/una  {} dell'elemento nel terreno.".format(get_nome_elemento(nome) , livello_tessuti_fogliari)) 
        print(str.upper("terapia"))
        print("I dati raccolti fanno evincere che i livello del nutriente nei tessuti fogliari e' buono, quindi il problema può essere dovuto a una malattia della pianta , o a un parassita")
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
                Fact(livello_terreno = "grave carenza"),
                Fact(livello_terreno = "livello carente")
        ),
        NOT(Fact(livello_tessuti_fogliari = W())),
        Fact(livello_terreno = MATCH.livello_terreno),
        salience = 1
    )
    def stampa_diagnosi_5(self, nome, descrizione, livello_terreno):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del terreno"))
        print("L'analisi delle percentuali di {} in mg/kg nel terreno , ha evidenziato un/una  {} dell'elemento nel terreno.".format(get_nome_elemento(nome) , livello_terreno))
        print(str.upper("terapia"))
        self.declare(Fact(terapia=si_o_no("Vuoi che ti venga proposta una possibile terapia")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        OR(
                Fact(livello_terreno = "livello normale"),
                Fact(livello_terreno = "eccesso")
        ),
        NOT(Fact(livello_tessuti_fogliari = W())),
        Fact(livello_terreno = MATCH.livello_terreno),
        salience = 1
    )
    def stampa_diagnosi_6(self, nome, descrizione, livello_terreno):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        print(str.upper("analisi del terreno"))
        print("L'analisi delle percentuali di {} in mg/kg nel terreno , ha evidenziato un/una  {} dell'elemento nel terreno.".format(get_nome_elemento(nome) , livello_terreno))
        print(str.upper("terapia"))
        print("I dati raccolti fanno evincere che i livello del nutriente nei tessuti fogliari e' buono, quindi il problema può essere dovuto a una malattia della pianta , o a un parassita")
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    @Rule(
        Diagnosi(nome=MATCH.nome , descrizione=MATCH.descrizione),
        NOT(Fact(livello_tessuti_fogliari = W())),
        NOT(Fact(livello_terreno = W())),
    )
    def stampa_diagnosi_7(self, nome , descrizione):
        print(str.upper("diagnosi"))
        print(str.upper(nome))
        print(descrizione)
        self.declare(Fact(terapia=si_o_no("Vuoi che ti venga proposta una possibile terapia")))

    """
    FINE DIAGNOSI
    """

    """
    NESSUNA DIAGNOSI
    """

    @Rule(
        NOT(Diagnosi(nome = W() , descrizione = W())),
        salience = 0
    )
    def no_diagnosi(self):
        print("Siamo spiacenti ma il sistema non e' riuscito a raggiungere una diagnosi")
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    """
    FINE NESSUNA DIAGNOSI
    """

    """
    ALTRE REGOLE
    """

    @Rule(
        Fact(terapia = "si"),
        Terapia(nome = MATCH.nome , descrizione = MATCH.descrizione)
        )
    def stampa_terapia_1(self, nome, descrizione):
        print(str.upper(nome))
        print(descrizione)
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    @Rule(
        Fact(terapia = "no"),
        )
    def stampa_terapia_2(self):
        self.declare(Fact(ripeti=si_o_no("Vuoi ripetere l'operazione per vedere se la pianta esaminata presenta altre carenze")))

    @Rule(
        Fact(ripeti = "si")
    )
    def ripeti(self):
       self.reset()
       self.run()


    """
    FINE ALTRE REGOLE
    """

engine = ExpertSystem()
engine.reset()
engine.run()
