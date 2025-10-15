#include "DHT.h"

// --- PINOS ---
#define PIN_DHT 4
#define TIPO_DHT DHT22
#define PIN_LDR 34
#define BTN_N 18
#define BTN_P 19
#define BTN_K 21
#define PIN_RELE 5
#define LED_VERDE 2  

// --- PARÂMETROS DA CULTURA ---
const float PH_MIN = 6.0;
const float PH_MAX = 7.0;
const int UMI_MIN = 65;
const int UMI_MAX = 80;

// --- OBJETOS ---
DHT dht(PIN_DHT, TIPO_DHT);

void setup() {
  Serial.begin(115200);
  Serial.println(">>> Irrigação Inteligente - Tomates <<<");
  Serial.println("Lendo sensores...");

  pinMode(BTN_N, INPUT_PULLUP);
  pinMode(BTN_P, INPUT_PULLUP);
  pinMode(BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  digitalWrite(PIN_RELE, LOW);
  digitalWrite(LED_VERDE, LOW);     
  dht.begin();
}

void loop() {
  float umi = dht.readHumidity();
  if (isnan(umi)) {
    Serial.println("Erro na leitura do DHT!");
    delay(2000);
    return;
  }

  bool n_ok = (digitalRead(BTN_N) == LOW);
  bool p_ok = (digitalRead(BTN_P) == LOW);
  bool k_ok = (digitalRead(BTN_K) == LOW);
  bool nutri_ok = n_ok && p_ok && k_ok;

  int ldr_valor = analogRead(PIN_LDR);
  float ph = map(ldr_valor, 0, 4095, 140, 0) / 10.0;
  bool ph_ok = (ph >= PH_MIN && ph <= PH_MAX);

  Serial.println("\n-----------------------------");
  Serial.print("Umidade: ");
  Serial.print(umi);
  Serial.println("%");

  Serial.print("Nutrientes: ");
  Serial.print(n_ok ? "[N OK] " : "[FALTA N] ");
  Serial.print(p_ok ? "[P OK] " : "[FALTA P] ");
  Serial.println(k_ok ? "[K OK] " : "[FALTA K] ");

  Serial.print("pH: ");
  Serial.print(ph);
  Serial.println(ph_ok ? " (Ideal)" : " (Fora do ideal)");
  Serial.println("-----------------------------");

  Serial.print("Bomba: ");

  if (umi < UMI_MIN && nutri_ok && ph_ok) {
    Serial.println("LIGADA (condições ideais)");
    digitalWrite(PIN_RELE, HIGH);
  }
  
  else if (umi > UMI_MAX) {
    Serial.println("DESLIGADA (solo saturado)");
    digitalWrite(PIN_RELE, LOW);
  }
  else if (umi >= UMI_MIN) {
    Serial.println("DESLIGADA (umidade do solo adequada)");
    digitalWrite(PIN_RELE, LOW);
  }
  else if (!nutri_ok) {
    Serial.println("DESLIGADA (corrija os níveis de nutrientes)");
    digitalWrite(PIN_RELE, LOW);
  }
  else if (!ph_ok) {
    Serial.println("DESLIGADA (pH do solo fora da faixa ideal)");
    digitalWrite(PIN_RELE, LOW);
  }
  
  else {
    Serial.println("DESLIGADA (aguardando condições)");
    digitalWrite(PIN_RELE, LOW);
  }

  delay(2000);
}
