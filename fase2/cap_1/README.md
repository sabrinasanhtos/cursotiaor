#  Fase 2 Cap 1
### Sistema de Irrigação Inteligente com ESP32, Sensores Simulados e Integração Python

---

##  **Descrição do Projeto**

O sistema utiliza **sensores simulados** para representar medições reais do campo agrícola e, opcionalmente, integra dados meteorológicos de uma **API pública** (como OpenWeather) para otimizar o uso da água.

---

##  **Componentes e Simulações**

| Elemento Real | Componente Simulado | Função |
|----------------|----------------------|---------|
| Sensor de Nitrogênio (N) | Botão verde (Digital) | Detecta nível de Nitrogênio (pressionado = alto) |
| Sensor de Fósforo (P) | Botão verde (Digital) | Detecta nível de Fósforo |
| Sensor de Potássio (K) | Botão verde (Digital) | Detecta nível de Potássio |
| Sensor de pH do solo | Sensor LDR (Analógico) | Simula leitura de pH (0 a 14) |
| Sensor de Umidade do Solo | Sensor DHT22 | Mede a “umidade” simulada do solo |
| Bomba de irrigação | Relé azul | Liga/desliga conforme condições definidas |

---

## 🧠 **Lógica de Funcionamento**

1. O **ESP32** lê os estados dos três botões (N, P, K).  
2. O sensor **LDR** retorna um valor analógico (simulando o pH da terra).  
3. O **DHT22** fornece o valor de umidade (interpretado como umidade do solo).  
4. O sistema executa a **lógica de decisão**:  
   - Se os níveis de NPK estiverem dentro da faixa ideal e o pH for neutro,  
     o sistema verifica a umidade.  
   - Se a umidade estiver **abaixo do limite**, o **relé (bomba)** é acionado.  
   - Caso contrário, a bomba é desligada para evitar desperdício.

---

##  **Entregáveis**

- ✅ Código **C/C++ (ESP32)**: `sketch.ino`  
- ✅ **README.md** documentando toda a lógica  
- ✅ Imagem do circuito (Wokwi.com)  
- ✅ Link de vídeo (até 5 minutos, não listado no YouTube)

---

## **Imagens e Demonstração**

> Todas as imagens devem ser armazenadas dentro da pasta `fase2/cap_1/images/`.  
> Basta substituir os exemplos abaixo pelos nomes reais dos arquivos que você colocar nessa pasta.

### Circuito no Wokwi  
![Circuito Wokwi](fase2/cap_1/images/umidade.jpg)

### Simulação no ESP32  
![Simulação ESP32](fase2/cap_1/images/simulacao.jpg)

### Saída do Monitor Serial  
![Saída Serial](fase2/cap_1/images/saida_serial.jpg)


---

## 🧠 **Benefícios do Projeto**

- Aplicação prática de **IoT e automação agrícola**  
- Uso de **simulação realista no Wokwi (ESP32)**  

---

## 📺 **Demonstração em Vídeo**

> **Link YouTube:**  
> [https://youtu.be/Ei3gy2853O4?si=rSCjallT5ZxaF3wz](https://youtu.be/Ei3gy2853O4?si=rSCjallT5ZxaF3wz)  

> **Link Wokwi:**  
> [https://wokwi.com/projects/444826807799729153](https://wokwi.com/projects/444826807799729153)

