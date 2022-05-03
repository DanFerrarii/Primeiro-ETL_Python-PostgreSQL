import pandas as pd
from modules.graficos import Grafico
from modules.postgres import Conector_postgres

if __name__=="__main__":
    try:
        print("Conectando banco de dados")
        banco=Conector_postgres("XXX.X.X.X","nomeBD","user","password",) #Informações da conexão com o banco ("ip","nome do banco de dados","usuário","senha")
        
        escolha=input("Escolha o que você deseja fazer: \n1-Ler o CSV com um DF e inserir no BD \n2-Insights")
        
        if escolha=="1":   
            print("Lendo o CSV e colocando os dados em um DF")
            df=pd.read_csv("Caminho do CSV ("./Python/data/RefugiadosUcrania_Polonia.csv")
           
            print("Tratando dados")
            df1=df.drop(columns=["Border Guard Post", "Border Guard Unit","UE / Schengen"]) #Eliminando colunas desnecessárias para o objetivo
            df2=df1.dropna()

            print("Inserindo dados no BD")
            for i,x in df2.iterrows():
                banco.inserir(f"INSERT INTO refugiados (passagem_fronteira,via,data,direcao_polonia,cidadania,checkin,checkout) VALUES ( '{df2['Border crossing'][i]}', '{df2['Type of border crossing'][i]}', date '{df2['Date'][i]}', '{df2['Direction to / from Poland'][i]}', '{df2['Citizenship (code)'][i]}', {(df2['Number of persons (checked-in)'][i])}, {(df2['Number of people (evacuated)'][i])} )")    
            
            escolha="2"
            
        elif escolha=="2":
            print("\n-------------------------------------------------------------\n")
            while True:    
                escolha2=input("Escolha um insight: \n1-Refugiados por mês\n2-Via mais utilizada\n3-Refugiados Ucranianos x Refugiados outra cidadania\n4-Três maiores nacionalidades de refugiados\n5-Total de refugiados(com controle x sem controle de fronteira)\n6-Partiram da Polônia x Chegaram na Polônia\n7-Nº Refugiados antes x depois da guerra\n8-Cidades mais utilizadas pelos refugiados\n9-Dia com maior Nº de refugiados x Dia com menor Nº de refugiados (Durante a guerra)\n0-Sair")
                if escolha2=="1":
                    #Primeiro insight - Refugiados por mês
                    total_refugiados_jan=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) AS refugiados_jan FROM refugiados WHERE data BETWEEN '2022-01-01' AND '2022-01-31'")
                    total_refugiados_fev=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) AS efugiados_fev FROM refugiados WHERE data BETWEEN '2022-02-01' AND '2022-02-28'")
                    total_refugiados_marc=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) AS refugiados_marc FROM refugiados WHERE data BETWEEN '2022-03-01' AND '2022-03-31'")
                    
                    refugiados_mes=[total_refugiados_jan[0][0],total_refugiados_fev[0][0],total_refugiados_marc[0][0]]
                    meses=["Janeiro", "Fevereiro", "Março"]
                    valores_eixoY=[779194, 1303432, 3982831]
                    Grafico.plotBarra(meses,refugiados_mes,"blue","Refugiados/mês","Meses","Nº de Refugiados",None,valores_eixoY)

                elif escolha2=="2":
                    #Segundo insight - Via mais utilizada
                    vias=banco.selecionar(f"SELECT via,COUNT(via) as total FROM refugiados GROUP BY via")
                    eixox=[vias[0][0],vias[1][0]]
                    eixoy=[vias[0][1],vias[1][1]]
                    Grafico.plotBarra(eixox,eixoy,"red","Vias Utilizadas","Vias","Qtde utilizada")

                elif escolha2=="3":
                    #Terceiro insight - Refugiados Ucranianos x Refugiados outra cidadania
                    refugiados_ucranianos=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) FROM refugiados WHERE cidadania='UA'")
                    refugiados_outros=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) FROM refugiados WHERE cidadania!='UA'")
                    eixox=["Ucranianos","Outros"]
                    eixoy=[refugiados_ucranianos[0][0],refugiados_outros[0][0]]
                    valores_eixoY=[5624176,441281]
                    Grafico.plotBarra(eixox,eixoy,"yellow","Refugiados Ucranianos x Refugiados outra cidadania","Cidadania","Nº de Refugiados",None,valores_eixoY)
                
                elif escolha2=="4":
                    #Quarto insight - Três maiores nacionalidades de refugiados
                    maiores_cidadanias=banco.selecionar(f"SELECT cidadania,(SUM(checkin)+ SUM(checkout)) AS total FROM refugiados GROUP BY cidadania ORDER BY total DESC LIMIT 3") 
                    eixox=[maiores_cidadanias[0][0],maiores_cidadanias[1][0],maiores_cidadanias[2][0]]
                    eixoy=[maiores_cidadanias[0][1],maiores_cidadanias[1][1],maiores_cidadanias[2][1]]
                    Grafico.plotBarra(eixox,eixoy,"purple","Três maiores nacionalidades de refugiados","Nacionalidades(UA-Ucraniano, PL-Polonês, DE-Alemão","Total de Refugiados")
                
                elif escolha2=="5":
                    #Quinto insight - Refugiados com controle de fronteiras x sem controle de fronteias
                    controle_fronteira=banco.selecionar(f"SELECT SUM(checkin) as checkin, SUM(checkout) as checkout FROM refugiados ")
                    eixox=["Com controle de fronteira","Sem controle de fronteira"]
                    eixoy=[controle_fronteira[0][0],controle_fronteira[0][1]]
                    Grafico.plotBarra(eixox,eixoy,"brown","Refugiados com controle de fronteiras x sem controle de fronteias",None,"Qtde de refugiados")
                
                elif escolha2=="6":
                    #Sexto insight - Patiram da Polônia  x Chegaram na Polônia 
                    partiu_polonia=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) as partiu_polonia FROM refugiados WHERE direcao_polonia='departure from Poland'")
                    chegou_polonia=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) as chegou_polonia FROM refugiados WHERE direcao_polonia='arrival in Poland'")
                    eixox=["Partiram da Polônia ","Chegaram na Polônia "]
                    eixoy=[partiu_polonia[0][0],chegou_polonia[0][0]]
                    Grafico.plotBarra(eixox,eixoy,"orange","Partiram da Polônia x Chegaram na Polônia ",None,"Qtde de refugiados")
                
                elif escolha2=="7":
                    #Sétimo insight - Nº Refugiados antes x depois da guerra
                    antes_guerra=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) AS refugiados_antes_guerra FROM refugiados WHERE data BETWEEN '2022-01-01' AND '2022-02-23'")
                    depois_guerra=banco.selecionar(f"SELECT (SUM(checkin)+ SUM(checkout)) AS refugiados_depois_guerra FROM refugiados WHERE data BETWEEN '2022-02-24' AND '2022-03-31'")
                    eixox=["Antes da Guerra","Depois da Guerra"]
                    eixoy=[antes_guerra[0][0],depois_guerra[0][0]]
                    Grafico.plotBarra(eixox,eixoy,"black", "Refugiados antes e depois da guerra",None,"Qtde de refugiados")
                
                elif escolha2=="8":
                    #Oitavo insight - Cidades mais utilizadas pelos refugiados
                    cidades_utilizadas=banco.selecionar(f"SELECT passagem_fronteira, (SUM(checkin)+ SUM(checkout)) as qtde FROM refugiados GROUP BY passagem_fronteira ORDER BY qtde DESC")
                    eixox=[cidades_utilizadas[0][0],cidades_utilizadas[1][0],cidades_utilizadas[2][0],cidades_utilizadas[3][0],cidades_utilizadas[4][0],cidades_utilizadas[5][0]]
                    
                    eixoy=[cidades_utilizadas[0][1],cidades_utilizadas[1][1],cidades_utilizadas[2][1],cidades_utilizadas[3][1],cidades_utilizadas[4][1],cidades_utilizadas[5][1]]
                    
                    Grafico.plotBarra(eixox,eixoy,"blue","Cidades mais utilizadas pelos refugiados","Cidades","Qtde Refugiados")
                    
                elif escolha2=="9":
                    #Nono insight - Dia com maior Nº de refugiados x Dia com menor Nº de refugiados (Durante a guerra)
                    dia_maior=banco.selecionar(f"SELECT data, (SUM(checkin)+ SUM(checkout)) AS refugiados_depois_guerra FROM refugiados WHERE data BETWEEN '2022-02-24' AND '2022-03-31' GROUP BY data ORDER BY refugiados_depois_guerra DESC LIMIT 1")
                    
                    dia_menor=banco.selecionar(f"SELECT data, (SUM(checkin)+ SUM(checkout)) AS refugiados_depois_guerra FROM refugiados WHERE data BETWEEN '2022-02-24' AND '2022-03-31' GROUP BY data ORDER BY refugiados_depois_guerra ASC LIMIT 1")

                    eixox=[str(dia_maior[0][0]),str(dia_menor[0][0])]
                    eixoy=[dia_maior[0][1],dia_menor[0][1]]
                    
                    Grafico.plotBarra(eixox,eixoy,"red"," Dia maior Nº de refugiados x Dia menor Nº de refugiados (Durante a guerra)","Datas","Qtde de Refugiados")
                
                elif escolha2=="0":
                    break
                
                else:
                    print("-------------------------------------------------------------")
                    print("Escolha uma opção válida")
                    print("-------------------------------------------------------------")
    except Exception as e:
        print(str(e))
