from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import unittest

@dataclass
class ResultadoMemoria:
    algoritmo: str
    referencias: List[int]
    quantidade_frames: int
    hits: int
    page_faults: int
    substituicoes: int
    historico: List[dict]

    @property
    def total(self) -> int:
        return len(self.referencias)

    @property
    def taxa_hits(self) -> float:
        return self.hits / self.total * 100 if self.total else 0.0

    @property
    def taxa_page_faults(self) -> float:
        return self.page_faults / self.total * 100 if self.total else 0.0

def fifo(referencias: List[int], quantidade_frames: int) -> ResultadoMemoria:
    if quantidade_frames <= 0:
        raise ValueError('A quantidade de frames deve ser maior que zero.')
    if not referencias:
        raise ValueError('Informe ao menos uma referência de página.')
    frames: List[int] = []
    fila = deque()
    hits = page_faults = substituicoes = 0
    historico = []
    for pagina in referencias:
        substituida: Optional[int] = None
        if pagina in frames:
            hits += 1
            status = 'HIT'
        else:
            page_faults += 1
            status = 'PAGE FAULT'
            if len(frames) < quantidade_frames:
                frames.append(pagina)
                fila.append(pagina)
            else:
                substituida = fila.popleft()
                indice = frames.index(substituida)
                frames[indice] = pagina
                fila.append(pagina)
                substituicoes += 1
        historico.append({'pagina': pagina, 'status': status, 'frames': frames.copy(), 'substituida': substituida})
    return ResultadoMemoria('FIFO', referencias.copy(), quantidade_frames, hits, page_faults, substituicoes, historico)

def lru(referencias: List[int], quantidade_frames: int) -> ResultadoMemoria:
    if quantidade_frames <= 0:
        raise ValueError('A quantidade de frames deve ser maior que zero.')
    if not referencias:
        raise ValueError('Informe ao menos uma referência de página.')
    frames: List[int] = []
    ultima_utilizacao: Dict[int, int] = {}
    hits = page_faults = substituicoes = 0
    historico = []
    for instante, pagina in enumerate(referencias):
        substituida: Optional[int] = None
        if pagina in frames:
            hits += 1
            status = 'HIT'
        else:
            page_faults += 1
            status = 'PAGE FAULT'
            if len(frames) < quantidade_frames:
                frames.append(pagina)
            else:
                substituida = min(frames, key=lambda p: ultima_utilizacao[p])
                indice = frames.index(substituida)
                frames[indice] = pagina
                substituicoes += 1
        ultima_utilizacao[pagina] = instante
        historico.append({'pagina': pagina, 'status': status, 'frames': frames.copy(), 'substituida': substituida})
    return ResultadoMemoria('LRU', referencias.copy(), quantidade_frames, hits, page_faults, substituicoes, historico)

def exibir_resultado(resultado: ResultadoMemoria) -> None:
    print(f'\n--- Resultado {resultado.algoritmo} ---')
    print(f'Referências: {resultado.referencias}')
    print(f'Quantidade de frames: {resultado.quantidade_frames}')
    print('\nPágina | Status       | Frames                | Substituída')
    print('-' * 66)
    for etapa in resultado.historico:
        frames = str(etapa['frames'])
        substituida = str(etapa['substituida']) if etapa['substituida'] is not None else '-'
        print(f"{etapa['pagina']:>6} | {etapa['status']:<12} | {frames:<21} | {substituida}")
    print('\nResumo:')
    print(f'HITs: {resultado.hits}')
    print(f'PAGE FAULTs: {resultado.page_faults}')
    print(f'Substituições: {resultado.substituicoes}')
    print(f'Taxa de HITs: {resultado.taxa_hits:.2f}%')
    print(f'Taxa de PAGE FAULTs: {resultado.taxa_page_faults:.2f}%')

def comparar_fifo_lru(referencias: List[int], quantidade_frames: int) -> None:
    resultado_fifo = fifo(referencias, quantidade_frames)
    resultado_lru = lru(referencias, quantidade_frames)
    print('\n=== COMPARAÇÃO FIFO x LRU ===')
    print(f"{'Métrica':<25}{'FIFO':>12}{'LRU':>12}")
    print('-' * 49)
    print(f"{'HITs':<25}{resultado_fifo.hits:>12}{resultado_lru.hits:>12}")
    print(f"{'PAGE FAULTs':<25}{resultado_fifo.page_faults:>12}{resultado_lru.page_faults:>12}")
    print(f"{'Substituições':<25}{resultado_fifo.substituicoes:>12}{resultado_lru.substituicoes:>12}")
    print(f"{'Taxa de HITs (%)':<25}{resultado_fifo.taxa_hits:>12.2f}{resultado_lru.taxa_hits:>12.2f}")

def analisar_belady(referencias: List[int], frames_lista: List[int]) -> List[Tuple[int, int]]:
    if not frames_lista or any((q <= 0 for q in frames_lista)):
        raise ValueError('Informe quantidades de frames maiores que zero.')
    resultados = []
    print('\n=== ANÁLISE DA ANOMALIA DE BELADY (FIFO) ===')
    print(f'Referências: {referencias}')
    print(f"{'Frames':<12}{'Page Faults':<15}")
    print('-' * 27)
    for quantidade in frames_lista:
        resultado = fifo(referencias, quantidade)
        resultados.append((quantidade, resultado.page_faults))
        print(f'{quantidade:<12}{resultado.page_faults:<15}')
    anomalia = False
    for i in range(1, len(resultados)):
        if resultados[i][0] > resultados[i - 1][0] and resultados[i][1] > resultados[i - 1][1]:
            anomalia = True
            print(f'\nAnomalia identificada: ao aumentar de {resultados[i - 1][0]} para {resultados[i][0]} frames, as faltas aumentaram de {resultados[i - 1][1]} para {resultados[i][1]}.')
    if not anomalia:
        print('\nNenhuma anomalia foi identificada entre as quantidades comparadas.')
    return resultados

def encontrar_ciclo(grafo: Dict[str, Set[str]]) -> Optional[List[str]]:
    estado: Dict[str, int] = {}
    pilha: List[str] = []
    posicao: Dict[str, int] = {}
    vertices = set(grafo)
    for vizinhos in grafo.values():
        vertices.update(vizinhos)

    def visitar(no: str) -> Optional[List[str]]:
        estado[no] = 1
        posicao[no] = len(pilha)
        pilha.append(no)
        for vizinho in grafo.get(no, set()):
            if estado.get(vizinho, 0) == 0:
                ciclo = visitar(vizinho)
                if ciclo:
                    return ciclo
            elif estado.get(vizinho) == 1:
                return pilha[posicao[vizinho]:] + [vizinho]
        pilha.pop()
        posicao.pop(no, None)
        estado[no] = 2
        return None
    for no in vertices:
        if estado.get(no, 0) == 0:
            ciclo = visitar(no)
            if ciclo:
                return ciclo
    return None

def simular_deadlock() -> None:
    print('\n=== SIMULAÇÃO DE DEADLOCK ===')
    print('Informe as dependências entre processos.')
    print('Exemplo: P1 P2 significa que P1 está esperando por P2.')
    print("Digite 'fim' quando terminar.")
    grafo: Dict[str, Set[str]] = {}
    while True:
        linha = input('Dependência: ').strip()
        if linha.lower() == 'fim':
            break
        partes = linha.split()
        if len(partes) != 2:
            print('Formato inválido. Digite dois processos, por exemplo: P1 P2.')
            continue
        origem, destino = partes
        grafo.setdefault(origem, set()).add(destino)
        grafo.setdefault(destino, set())
    ciclo = encontrar_ciclo(grafo)
    if ciclo:
        print('\nDEADLOCK IDENTIFICADO!')
        print('Ciclo de espera: ' + ' -> '.join(ciclo))
        print('Os processos desse ciclo estão aguardando uns pelos outros.')
    else:
        print('\nNenhum ciclo encontrado. Não foi identificado deadlock no grafo informado.')

class TestesSimulador(unittest.TestCase):

    def test_fifo_conta_hits_e_page_faults(self):
        resultado = fifo([1, 2, 1, 3], 2)
        self.assertEqual(resultado.hits, 1)
        self.assertEqual(resultado.page_faults, 3)
        self.assertEqual(resultado.substituicoes, 1)

    def test_lru_conta_hits_e_page_faults(self):
        resultado = lru([1, 2, 1, 3], 2)
        self.assertEqual(resultado.hits, 1)
        self.assertEqual(resultado.page_faults, 3)
        self.assertEqual(resultado.substituicoes, 1)

    def test_fifo_anomalia_de_belady(self):
        referencias = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        self.assertEqual(fifo(referencias, 3).page_faults, 9)
        self.assertEqual(fifo(referencias, 4).page_faults, 10)

    def test_detecta_deadlock(self):
        grafo = {'P1': {'P2'}, 'P2': {'P3'}, 'P3': {'P1'}}
        self.assertIsNotNone(encontrar_ciclo(grafo))

    def test_nao_detecta_ciclo(self):
        grafo = {'P1': {'P2'}, 'P2': {'P3'}, 'P3': set()}
        self.assertIsNone(encontrar_ciclo(grafo))

    def test_quantidade_frames_invalida(self):
        with self.assertRaises(ValueError):
            fifo([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            lru([1, 2, 3], -1)

def executar_testes() -> None:
    print('\n=== EXECUTANDO TESTES AUTOMATIZADOS ===')
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestesSimulador)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    if resultado.wasSuccessful():
        print('\nTodos os testes passaram.')
    else:
        print('\nAlguns testes falharam. Verifique as mensagens acima.')

def ler_referencias() -> List[int]:
    texto = input('Digite as páginas separadas por espaço (ex.: 1 2 3 1 4 2 5): ').strip()
    try:
        referencias = [int(item) for item in texto.split()]
    except ValueError:
        raise ValueError('As páginas devem ser números inteiros.')
    if not referencias:
        raise ValueError('Informe ao menos uma página.')
    if any((pagina < 0 for pagina in referencias)):
        raise ValueError('As páginas devem ser números inteiros não negativos.')
    return referencias

def menu() -> None:
    while True:
        print('\n' + '=' * 54)
        print(' SIMULADOR DE SISTEMAS OPERACIONAIS COM PYTHON')
        print('=' * 54)
        print('1 - Simular FIFO')
        print('2 - Simular LRU')
        print('3 - Comparar FIFO e LRU')
        print('4 - Analisar anomalia de Belady')
        print('5 - Simular detecção de deadlock')
        print('6 - Executar testes automatizados')
        print('0 - Sair')
        opcao = input('Escolha uma opção: ').strip()
        try:
            if opcao == '1':
                referencias = ler_referencias()
                frames = int(input('Quantidade de frames: '))
                exibir_resultado(fifo(referencias, frames))
            elif opcao == '2':
                referencias = ler_referencias()
                frames = int(input('Quantidade de frames: '))
                exibir_resultado(lru(referencias, frames))
            elif opcao == '3':
                referencias = ler_referencias()
                frames = int(input('Quantidade de frames: '))
                comparar_fifo_lru(referencias, frames)
            elif opcao == '4':
                referencias = ler_referencias()
                texto = input('Quantidades de frames separadas por espaço (ex.: 3 4): ')
                frames_lista = [int(item) for item in texto.split()]
                analisar_belady(referencias, frames_lista)
            elif opcao == '5':
                simular_deadlock()
            elif opcao == '6':
                executar_testes()
            elif opcao == '0':
                print('Encerrando o simulador. Até mais!')
                break
            else:
                print('Opção inválida. Escolha uma opção do menu.')
        except ValueError as erro:
            print(f'Entrada inválida: {erro}')
if __name__ == '__main__':
    menu()
