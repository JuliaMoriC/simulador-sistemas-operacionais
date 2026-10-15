# Simulador de Sistemas Operacionais

Projeto acadêmico em Python sobre deadlock e gerenciamento de memória.

## Arquivos

- `atividade_sistemas_operacionais.ipynb`: notebook para abrir e executar célula por célula no VS Code ou Google Colab.
- `simulador_sistemas_operacionais.py`: versão executável pelo terminal com menu interativo.

## Como abrir no VS Code

1. Extraia o arquivo ZIP.
2. Abra o VS Code.
3. Vá em **Arquivo > Abrir Pasta** e selecione a pasta `simulador-sistemas-operacionais`.
4. Para executar o notebook, abra `atividade_sistemas_operacionais.ipynb`. Se solicitado, instale/ative as extensões Python e Jupyter.
5. Clique em **Run All / Executar Tudo** para executar as células em ordem.

## Como executar o arquivo Python

Abra o terminal integrado do VS Code e execute:

```bash
python simulador_sistemas_operacionais.py
```

No menu, escolha uma opção para testar FIFO, LRU, comparação dos algoritmos, anomalia de Belady, deadlock ou testes automatizados.

## Conteúdo implementado

- Algoritmo FIFO
- Algoritmo LRU
- Contagem de HITs, PAGE FAULTs e substituições
- Comparação FIFO x LRU
- Anomalia de Belady
- Detecção de ciclos em grafo de espera para identificar deadlock
- Testes automatizados
