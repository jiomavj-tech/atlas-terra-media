# Regras para agentes (Codex, Claude e outros)

Este repositório guarda o **Atlas da Terra-média**: um aplicativo de **arquivo único** (`index.html`, cerca de 2 MB) sobre o universo de Tolkien. O dono usa principalmente pelo **Chrome no Android**. Ele não é programador, então descreva as mudanças em português simples.

## Como trabalhar

1. **Uma tarefa por pull request.** As tarefas ficam em `TAREFAS.md`. Cite o número no título do PR, por exemplo: `Tarefa 1 — Grafo principal não abre`.
2. **Antes de abrir o PR, rode o teste de fumaça** e cole o resultado na descrição:
   ```
   pip install playwright
   python -m playwright install chromium
   python tools/teste_fumaca.py
   ```
   O PR não pode criar erros novos no teste. Os erros que a tarefa resolve têm que sumir da lista.
3. **Atualize o `CHANGELOG.md`** com uma linha por mudança, em português.
4. **Não mude a versão.** Ela fica num lugar só, `window.ATLAS_VERSAO` no `<head>`, e o título e o cabeçalho leem dali. Quem troca o número, ao juntar os PRs, é o revisor.

## O que NÃO fazer

- **Não divida o `index.html`** em vários arquivos, nem converta para React, Vue, TypeScript ou outro framework.
- **Não adicione bibliotecas nem CDNs externas.** O Atlas precisa funcionar offline.
- **Não reescreva o arquivo inteiro.** Ele tem linhas enormes e imagens embutidas em base64. Faça substituições pontuais, por exemplo com um script Python que troca um trecho exato e confere que o trecho aparece só uma vez.
- **Não altere, recomprima nem remova as imagens embutidas** (`data:image/...`). Os retratos já foram revisados pelo dono.
- **Não apague seções, conteúdo nem dados de personagens**, a menos que a tarefa peça.
- **Não reative animações contínuas.** Elas foram desligadas porque travavam no Android.

## Estrutura do app

- Navegação (v8.5): o leitor vê **9 seções** (`#atlasNavGroup` no topo) com **abas** (`#atlasNavTabs`) e a barra inferior Início · Pessoas · Teia · Mapa · História · ☰ Mais (`#atlasNavMore`). A lista de seções/abas fica no array `G` do script `atlas-v85-nav-script`.
- Por dentro continuam existindo as 20 seções antigas: o `#atlasUxSelect` (escondido) troca a seção, e a ativa fica em `document.body.dataset.view`. Para abrir uma seção por código, mude `#atlasUxSelect` e dispare `change`. O "Comparador de obras" (`#comparador`) foi juntado embaixo de `#comparador-adaptacoes` (aba "Comparar").
- Cada seção é um `<section id="...">` dentro do `<body>`.
- A voz (busca e leitura) fica no bloco `#atlasVoice`, no fim do arquivo, e é exposta como `window.AtlasVoz`.
- O mapa ilustrado está em `#mapas-originais`, com os pontos em `#atlasMapPins`. O modo 3D é o bloco `#atlasMap3D` (`window.AtlasMapa3D`); o relevo é o script `atlas-v86-relevo` (`window.AtlasRelevo`, WebGL puro). Arquivos do relevo em `tools/relevo/`: `limpar_textura.py` (tira nomes, ícones e botões pintados do mapa → constante `TEX`), `gerar_relevo.py` (altitude: cordilheiras traçadas à mão + montanhas detectadas na imagem) e `assar_luz.py` (sombras projetadas, oclusão e água → canais G e B da constante `HM`). Rode na ordem: limpar → gerar → assar.
- A Teia Viva está em `#teia-viva`. No celular ela roda em "modo leve" (`.atlas-litelist`).
- Os retratos ficam em `#atlas-portraits`. O evento `atlas:open-person` abre a ficha de um personagem.

## Regiões de detalhe do mapa 3D

- Cada região é um `<script id="atlas-detail-...">` que faz `window.ATLAS_DETAILS.push({rect,hm,tex,models,trees})`. O motor (`AtlasRelevo`) troca o terreno dentro de `rect` por uma malha própria, permite zoom até `zFit*110` ali e desenha os `models` (`smial`, `house`, `bigsmial`, `inn`, `mill`, `bridge`, `ferry`, `jetty`, `tree_big`, `stone`, `hay`, `sheep`, `fence`, `hedge`, `gate`).
- Tipos com altura absoluta (usados em Minas Tirith): `cylA`, `capA`, `boxA`, `houseA`, `polyA`, `discA`, `blobA`, `treeW`; e ainda `cyl`, `box`, `wall`, `boat`. `tops` dá a altura dos nomes de perto.
- Valfenda é gerada por `tools/relevo/desenhar_valfenda.py` e embutida por `embutir_valfenda.py`. O motor aceita até 4 regiões (`drc[4]`): hoje são Condado, Minas Tirith, Valfenda e Montanha da Perdição (`desenhar_montanha_perdicao.py`). Para uma 5ª, aumente o tamanho de `drc` no shader.
- Minas Tirith é gerada por `tools/relevo/desenhar_minas_tirith.py` e embutida por `embutir_minas_tirith.py`.
- O Condado é gerado por `tools/relevo/desenhar_condado.py` (depende das saídas de `desenhar_terra_media.py` e `assar_terra_media.py`). Os nomes de perto ficam em `PINS` (marcados em `SUBK`).

## Instalação (PWA)

- `manifest.webmanifest`, `sw.js` e os ícones `icon-*.png` permitem instalar o Atlas no Android. O `sw.js` usa "rede primeiro": com internet sempre baixa a versão nova; sem internet abre a última cópia. Ao mudar a lista de arquivos guardados, troque o nome do `CACHE`.

## Idioma

Os textos visíveis ficam em **português do Brasil**. Os nomes seguem a tradução brasileira de Tolkien (Bolseiro, Valfenda, Montanha da Perdição).
