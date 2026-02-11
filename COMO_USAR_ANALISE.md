# 🎯 Como Analisar Suas Apostas do Concurso 3610

## Resultado do Concurso 3610
```
01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25
```

## ✅ Scripts Criados

Criei **dois scripts** para você analisar suas apostas:

### 1. 🚀 Script Rápido: `analisar_concurso_3610.py`

**Recomendado para começar!**

Este script é específico para o concurso 3610 e permite entrada manual dos seus jogos.

#### Como usar:

```bash
python analisar_concurso_3610.py
```

Quando executar, o script vai pedir para você digitar seus jogos:

```
Digite seus jogos (números separados por vírgula):
Jogo 1: 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15
Jogo 2: 16,17,18,19,20,21,22,23,24,25,01,02,03,04,05
```

Digite `fim` quando terminar.

---

### 2. 🖼️ Script com OCR: `analisar_apostas_imagem.py`

Este script pode **extrair números automaticamente de uma imagem** usando tecnologia OCR.

#### Opção A: Usar uma imagem

```bash
python analisar_apostas_imagem.py caminho/sua_imagem.jpg 3610 "01,03,05,07,08,10,13,14,17,20,21,22,23,24,25"
```

#### Opção B: Modo interativo

```bash
python analisar_apostas_imagem.py
```

O script perguntará:
- Se você tem uma imagem (s/n)
- Se sim: caminho da imagem
- Número do concurso: `3610`
- Números do resultado: `01,03,05,07,08,10,13,14,17,20,21,22,23,24,25`

Se o OCR não conseguir ler a imagem, você pode digitar manualmente.

---

## 📸 Sobre a Imagem

Você mencionou que tem **dois jogos em uma imagem**. Para o script funcionar melhor:

1. **Tire uma foto clara** da sua aposta
2. **Boa iluminação** ajuda muito
3. **Números devem estar visíveis**
4. Formatos aceitos: JPG, PNG, BMP, TIFF

Se o OCR não funcionar perfeitamente, **não se preocupe** - você pode digitar os números manualmente quando o script perguntar!

---

## 📋 Exemplo de Resultado

Quando você executar o script, verá algo assim:

```
================================================================================
ANÁLISE DE APOSTAS - CONCURSO 3610
================================================================================

Resultado: 01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25

────────────────────────────────────────────────────────────────────────────────
JOGO 1
────────────────────────────────────────────────────────────────────────────────
Números: 01, 03, 05, 07, 08, 10, 13, 14, 17, 18, 19, 20, 21, 22, 23

✨ TREZE PONTOS! (13 acertos)

Acertou: 01, 03, 05, 07, 08, 10, 13, 14, 17, 20, 21, 22, 23
Errou:   18, 19

────────────────────────────────────────────────────────────────────────────────
JOGO 2
────────────────────────────────────────────────────────────────────────────────
Números: 02, 03, 05, 07, 08, 10, 12, 14, 17, 20, 21, 22, 23, 24, 25

✨ TREZE PONTOS! (13 acertos)

Acertou: 03, 05, 07, 08, 10, 14, 17, 20, 21, 22, 23, 24, 25
Errou:   02, 12
```

---

## 🎯 Níveis de Premiação

| Acertos | Descrição | Emoji |
|---------|-----------|-------|
| 15 | QUINZE PONTOS! | 🎯 |
| 14 | QUATORZE PONTOS! | ⭐ |
| 13 | TREZE PONTOS! | ✨ |
| 12 | DOZE PONTOS! | 🌟 |
| 11 | ONZE PONTOS! | 💫 |
| < 11 | Não premiado | ❌ |

---

## 🚀 Começando Agora

### Método mais fácil (sem imagem):

```bash
python analisar_concurso_3610.py
```

Depois é só digitar seus jogos quando pedir!

### Com imagem:

1. Salve sua imagem de aposta no computador
2. Execute: `python analisar_apostas_imagem.py`
3. Escolha "s" quando perguntar sobre imagem
4. Digite o caminho da imagem
5. Digite: `3610` para o concurso
6. Digite: `01,03,05,07,08,10,13,14,17,20,21,22,23,24,25` para o resultado

---

## 📖 Documentação Completa

Para mais detalhes, veja:
- [GUIA_ANALISE_APOSTAS.md](GUIA_ANALISE_APOSTAS.md) - Guia completo
- [README.md](README.md) - Documentação geral do projeto

---

## ❓ Precisa de Ajuda?

Se tiver problemas:
1. Tente o script simples primeiro (`analisar_concurso_3610.py`)
2. Use entrada manual se o OCR não funcionar
3. Verifique se todos os números estão no formato correto (separados por vírgula)

**Boa sorte! 🍀**
