# 🎯 Guia de Análise de Apostas

Este guia explica como usar os scripts de análise de apostas da Lotofácil.

## 📋 Scripts Disponíveis

### 1. `analisar_concurso_3610.py` - Análise Rápida do Concurso 3610

Script simplificado para analisar rapidamente seus jogos contra o resultado do concurso 3610.

**Resultado do Concurso 3610:**
```
01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25
```

#### Como usar:

```bash
python analisar_concurso_3610.py
```

O script irá solicitar que você digite seus jogos. Digite os números separados por vírgula:

```
Jogo 1: 01,03,05,07,08,10,13,14,17,18,19,20,21,22,23
Jogo 2: 02,03,05,07,08,10,12,14,17,20,21,22,23,24,25
```

Digite `fim` quando terminar de inserir seus jogos.

#### Exemplo de saída:

```
================================================================================
RESULTADOS DA ANÁLISE
================================================================================

────────────────────────────────────────────────────────────────────────────────
JOGO 1
────────────────────────────────────────────────────────────────────────────────
Números: 01, 03, 05, 07, 08, 10, 13, 14, 17, 18, 19, 20, 21, 22, 23

✨ TREZE PONTOS! (13 acertos)

Acertou: 01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23
Errou:   18, 19
```

---

### 2. `analisar_apostas_imagem.py` - Análise com Extração de Imagem (OCR)

Script completo que permite extrair números de apostas diretamente de uma imagem usando OCR (Reconhecimento Óptico de Caracteres).

#### Requisitos:

- Tesseract OCR instalado no sistema
- Bibliotecas Python: Pillow e pytesseract

#### Instalação do Tesseract:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Baixe e instale de: https://github.com/UB-Mannheim/tesseract/wiki

#### Como usar:

**Modo 1: Com argumentos de linha de comando**

```bash
python analisar_apostas_imagem.py caminho/imagem.jpg 3610 "01,03,05,07,08,10,13,14,17,20,21,22,23,24,25"
```

**Modo 2: Modo interativo**

```bash
python analisar_apostas_imagem.py
```

O script perguntará:
1. Se deseja extrair de uma imagem (s/n)
2. Caminho da imagem (se sim)
3. Número do concurso
4. Números do resultado

**Modo 3: Entrada manual (se OCR falhar)**

Se o OCR não conseguir extrair os números automaticamente, o script oferecerá a opção de entrada manual.

#### Formatos de imagem suportados:

- JPG/JPEG
- PNG
- BMP
- TIFF
- GIF

#### Dicas para melhor reconhecimento OCR:

1. Use imagens com boa resolução
2. Certifique-se de que os números estejam claramente visíveis
3. Evite imagens com muita sombra ou reflexo
4. Quanto mais nítida a imagem, melhor o reconhecimento

---

## 🎲 Entendendo os Resultados

### Níveis de Premiação

| Acertos | Descrição |
|---------|-----------|
| 15 | 🎯 QUINZE PONTOS! |
| 14 | ⭐ QUATORZE PONTOS! |
| 13 | ✨ TREZE PONTOS! |
| 12 | 🌟 DOZE PONTOS! |
| 11 | 💫 ONZE PONTOS! |
| < 11 | ❌ Não premiado |

### Informações Exibidas

Para cada jogo analisado, você verá:

- **Números apostados**: Todos os 15 números do seu jogo
- **Resultado**: Nível de premiação e quantidade de acertos
- **Acertou**: Números que coincidiram com o resultado
- **Errou**: Números que você apostou mas não saíram

---

## 📝 Exemplos de Uso

### Exemplo 1: Análise simples do concurso 3610

```bash
$ python analisar_concurso_3610.py

Digite seus jogos (números separados por vírgula):
Jogo 1: 01,03,05,07,08,10,13,14,17,20,21,22,23,24,25
Jogo 2: fim

JOGO 1
Números: 01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25
🎯 QUINZE PONTOS! (15 acertos)
Acertou: 01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25
```

### Exemplo 2: Análise com imagem

```bash
$ python analisar_apostas_imagem.py minha_aposta.jpg 3610 "01,03,05,07,08,10,13,14,17,20,21,22,23,24,25"

Extraindo jogos da imagem: minha_aposta.jpg
Aguarde...

✓ 2 jogo(s) extraído(s) da imagem com sucesso!

[Resultados...]
```

### Exemplo 3: Análise de outro concurso

```bash
$ python analisar_apostas_imagem.py

Modo Interativo
Deseja extrair jogos de uma imagem? (s/n): n
Número do concurso: 3611
Números do resultado: 02,04,06,08,10,11,12,15,17,18,19,21,23,24,25

Digite seus jogos...
```

---

## ⚠️ Notas Importantes

1. **Formato dos números**: Sempre use 15 números separados por vírgula
2. **Números válidos**: Apenas números de 1 a 25
3. **Sem duplicatas**: Cada número pode aparecer apenas uma vez por jogo
4. **OCR não é 100% preciso**: Sempre confira os números extraídos da imagem
5. **Entrada manual**: Disponível como alternativa se o OCR falhar

---

## 🆘 Solução de Problemas

### Erro: "Bibliotecas não instaladas"
```bash
pip install -r requirements.txt
```

### Erro: "Tesseract not found"
Instale o Tesseract OCR no sistema (veja seção de Instalação do Tesseract)

### OCR não reconhece números
- Tente melhorar a qualidade da imagem
- Use entrada manual como alternativa
- Certifique-se de que a imagem está bem iluminada e focada

### Formato inválido
Certifique-se de usar o formato correto:
```
01,02,03,04,05,06,07,08,09,10,11,12,13,14,15
```

---

## 💡 Dicas

1. **Organize seus jogos**: Salve suas apostas em arquivos de texto para referência futura
2. **Tire fotos claras**: Use boa iluminação e foco para melhor reconhecimento OCR
3. **Verifique sempre**: Confira se os números extraídos estão corretos
4. **Use entrada manual**: Quando em dúvida, digite manualmente para garantir precisão

---

Para mais informações sobre o projeto, consulte o [README.md](README.md) principal.
