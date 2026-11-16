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

## Globo de Arda e zoom contínuo (v12.0)

- O globo (`#arStage`, script `atlas-arda-script`) é uma **camada dentro do `#m3Stage`**, não uma seção separada. O script `atlas-v105-arda-go-script` faz a passagem: `AtlasArdaGo.fromME()` e `toME()`.
- A Terra-média do mapa 3D está colada na textura do globo em **projeção ortográfica** centrada em lon 12°, lat 35°, com 36° de largura (`tools/relevo/desenhar_arda.py`). É isso que faz o globo coincidir com a vista de cima do mapa (`AtlasMapa3D.flatPose()`). Se mudar o mapa-base, rode `desenhar_arda.py` de novo.
- A seção antiga `atlas-arda` continua existindo só para redirecionar para o mapa com o globo aberto.
- Navegação: Mapa, Teia e Grafo 3D ficam no grupo `mapa` ("Explorar") do array `G`.

## Regiões de detalhe do mapa 3D

- Cada região é um `<script id="atlas-detail-...">` que faz `window.ATLAS_DETAILS.push({rect,hm,tex,models,trees})`. O motor (`AtlasRelevo`) troca o terreno dentro de `rect` por uma malha própria, permite zoom até `zFit*110` ali e desenha os `models` (`smial`, `house`, `bigsmial`, `inn`, `mill`, `bridge`, `ferry`, `jetty`, `tree_big`, `stone`, `hay`, `sheep`, `fence`, `hedge`, `gate`).
- Tipos com altura absoluta (usados em Minas Tirith): `cylA`, `capA`, `boxA`, `houseA`, `polyA`, `discA`, `blobA`, `treeW`; e ainda `cyl`, `box`, `wall`, `boat`. `tops` dá a altura dos nomes de perto.
- Valfenda é gerada por `tools/relevo/desenhar_valfenda.py` e embutida por `embutir_valfenda.py`. Não há limite de regiões (v11.0): o terreno-base é recortado por uma textura-máscara (`tMask`), e só as até `MAXG`=4 regiões mais próximas da câmera ficam na GPU (`wantDets`/`syncDets`). Use retângulos com coordenadas inteiras e malha de no máximo 65.535 vértices (`GR` × tamanho). Hoje há Condado, Minas Tirith, Valfenda e Montanha da Perdição (`desenhar_montanha_perdicao.py`). A partir da v11.1, as regiões novas usam `tools/relevo/regioes/reg.py`: a classe `Region` cuida de relevo, textura, luz e emenda com a base; `embed()` embute no `index.html`; `integrate()` acrescenta os nomes de perto, o mergulho e a rota. Já foram feitas com ela Isengard, Abismo de Helm, Edoras, Moria, Lothlórien, Bri, Topo do Vento, Portão Negro, Minas Morgul/Cirith Ungol, Erebor/Valle, Cidade do Lago, Dol Guldur, Fangorn, Rauros/Amon Hen, Portos Cinzentos, Fornost, Pelargir e Dol Amroth (23 regiões ao todo). Para lagos e mar, nivele a água na malha (veja `rauros.py` e `amroth.py`).
- Minas Tirith é gerada por `tools/relevo/desenhar_minas_tirith.py` e embutida por `embutir_minas_tirith.py`.
- O Condado é gerado por `tools/relevo/desenhar_condado.py` (depende das saídas de `desenhar_terra_media.py` e `assar_terra_media.py`). Os nomes de perto ficam em `PINS` (marcados em `SUBK`).

## Instalação (PWA)

- `manifest.webmanifest`, `sw.js` e os ícones `icon-*.png` permitem instalar o Atlas no Android. O `sw.js` usa "rede primeiro": com internet sempre baixa a versão nova; sem internet abre a última cópia. Ao mudar a lista de arquivos guardados, troque o nome do `CACHE`.

## Idioma

Os textos visíveis ficam em **português do Brasil**. Os nomes seguem a tradução brasileira de Tolkien (Bolseiro, Valfenda, Montanha da Perdição).
