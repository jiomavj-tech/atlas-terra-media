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

- Navegação: `#atlasUxSelect` (menu de seções) e `#atlasUxBottom` (barra inferior). A seção ativa fica em `document.body.dataset.view`.
- Cada seção é um `<section id="...">` dentro do `<body>`.
- A voz (busca e leitura) fica no bloco `#atlasVoice`, no fim do arquivo, e é exposta como `window.AtlasVoz`.
- O mapa ilustrado está em `#mapas-originais`, com os pontos em `#atlasMapPins`.
- A Teia Viva está em `#teia-viva`. No celular ela roda em "modo leve" (`.atlas-litelist`).
- Os retratos ficam em `#atlas-portraits`. O evento `atlas:open-person` abre a ficha de um personagem.

## Idioma

Os textos visíveis ficam em **português do Brasil**. Os nomes seguem a tradução brasileira de Tolkien (Bolseiro, Valfenda, Montanha da Perdição).
