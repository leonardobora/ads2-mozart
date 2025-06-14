# ADS2

## Aprendizado de Máquina - Atividade Discente Supervisionada 2  
**Prof. Mozart Hasse**

> **LEIA ATENTAMENTE TODAS AS INSTRUÇÕES ATÉ O FINAL DA ÚLTIMA PÁGINA. CADA PALAVRA CONTA!**

Use pelo menos os dados da base pública indicada pelo professor. Descubra tipos, faixas de valores e distribuições através de análise exploratória.

---

## Base de Dados

**Dataset:** Top 100 Songs & Lyrics By Year (1959–2023)  
**Fonte:** Kaggle  
Contém aproximadamente 6.500 músicas com letras completas.  
[Link para o dataset](https://www.kaggle.com/datasets/brianblakely/top-100-songs-and-lyrics-from-1959-to2019)

Ajustes adicionais poderão ser necessários dependendo do algoritmo escolhido. Fica a seu critério ajustar formatos ou remover campos, desde que cada previsão possa ser mapeada para a linha de origem. **Não é permitido enriquecer os dados com bases externas.**

A solução deste problema **DEVE OBRIGATORIAMENTE** ser buscada usando um algoritmo de aprendizado de máquina que **não envolva serviços externos** e que aplique algoritmos de redes neurais artificiais (**execução 100% na máquina local**). O professor está ciente que isso pode comprometer significativamente o resultado concreto obtido no caso de LLMs, mas o que se está avaliando é predominantemente o método escolhido (exemplo: prompts) e todo o processo realizado.

---

## Temas (Escolha UM)

- Detecção de conteúdo inapropriado: misoginia e/ou violência contra a mulher em letras de músicas populares (1959–2023)
- Detecção de conteúdo inapropriado: depressão e/ou validação ou incitação ao suicídio em letras de músicas populares (1959–2023)
- Detecção de conteúdo inapropriado: racismo, homofobia, discurso de ódio ou preconceito relacionado ao público LGBTQIAPN+ em letras de músicas populares (1959–2023)
- Detecção de conteúdo inapropriado: estímulo ou validação de relacionamentos tóxicos em letras de músicas populares (1959–2023)

---

## Objetivo

Aplicar técnicas de redes neurais e/ou LLMs (Large Language Models) para construir um modelo que classifique músicas (com base principalmente ou exclusivamente nas letras) de acordo com a presença de conteúdo vinculado ao tema escolhido pela equipe.

---

## Tarefa Principal

Criar um modelo de **classificação automática** que analisa letras de músicas e atribui uma **pontuação de intensidade do conteúdo inapropriado** na letra da música.  
A pontuação deve ser **contínua, com valor entre 0 e 1**, onde:

- **0**: música sem absolutamente nada (nem insinuação) de conteúdo inapropriado
- **1**: letra descreve conteúdo flagrantemente criminoso com perigo à ordem pública de acordo com a legislação atual

---

## Etapas Sugeridas para o Projeto

1. **Exploração do dataset**
    - Análise temporal: evolução da linguagem ao longo dos anos.
    - Metodologia de classificação: escolha dos critérios, coerência da pontuação e intensidade, compatibilidade dos critérios com a pontuação atribuída às músicas classificadas manualmente, completude dos mecanismos de detecção de conteúdo inapropriado, etc.
    - Frequência de palavras relacionadas a temas sensíveis.

2. **Construção de um conjunto rotulado**
    - Curadoria manual: cada grupo deve rotular manualmente pelos próprios critérios ao menos 30 músicas.
    - Uso de dicionários de termos ofensivos ou de qualquer forma violentos ou inadequados para apoio, incluindo sinônimos, expressões e analogias. Pode-se usar bases públicas específicas com estes termos para apoio.

3. **Abordagem com modelos**
    - Os alunos devem escolher ao menos uma dentre as abordagens abaixo:
        - LLMs como serviço LOCAL (OLLAMA) com prompt engineering envolvendo modelos PEQUENOS (0.5B a 7B), de acordo com a capacidade da máquina, ao menos na versão final.
        - Redes neurais recorrentes (RNNs, LSTM, GRU) ou CNNs para texto
        - Transformer simples (ex: DistilBERT)
        - Outra sugestão envolvendo redes neurais e validada pelo professor.

4. **Análise dos resultados**
    - Comparações entre anos: a linguagem e o teor nocivo das músicas piorou ou melhorou ao longo do tempo?
    - Visualizações: ranking das músicas mais problemáticas, heatmaps por ano, nuvem de palavras...

---

## Resultados Esperados

- Um **relatório técnico** explicando:
    - Escolhas metodológicas
    - Preprocessamento, bases complementares usadas e tratamentos específicos realizados
    - Técnicas de rotulagem (no mínimo uma referência que claramente apoie a escolha da gradação ou classificação, incluindo página ou parágrafo da fonte original)
    - Abordagem de modelagem
    - Limitações éticas e técnicas, incluindo, mas não se limitando a:
        - Analogias não triviais ou limitações na pontuação ou contexto da letra que foram identificados pela equipe
        - Ênfase dada pelo tom ou ritmo da música, que não tem como ser analisados nesta atividade
        - Poder de interpretação de vocabulário e contexto do modelo e/ou LLM escolhidos
        - Até onde é possível identificar conteúdo inadequado, destacando quais conteúdos não tem como ser identificados pelos critérios adotados
        - Outras limitações identificadas pela equipe
- Um **ranking das músicas NÃO ROTULADAS MANUALMENTE** com escore mais alto no tema escolhido.
- Um **notebook** com a apresentação final (storytelling) das visualizações e insights de forma organizada e sustentado ou direcionando alguma conclusão.
- Todas as referências seguindo as normas da **ABNT**.

---

## Critérios de Avaliação

- **Organização e clareza do código:** (30% da nota), incluindo comentários com a justificativa para as escolhas realizadas.
