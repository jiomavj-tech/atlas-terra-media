"""Teste de fumaça do Atlas da Terra-média.

Abre o index.html num Chromium sem tela, em tamanho de celular (400x800),
passa por todas as seções do menu, clica nos botões visíveis de cada uma
e lista os erros de JavaScript encontrados.

Uso:
    pip install playwright
    python -m playwright install chromium
    python tools/teste_fumaca.py            # testa ./index.html
    python tools/teste_fumaca.py outro.html

Saída: código 0 se não houver erros; 1 se houver.
"""
import collections
import pathlib
import sys

from playwright.sync_api import sync_playwright

ARQUIVO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()
PULAR_BOTOES = r"export|baixar|csv|download|limpar|apagar|excluir|remover"
MAX_BOTOES_POR_SECAO = 25


def main() -> int:
    erros = []
    secao_atual = ["carregamento"]
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 400, "height": 800})
        pg.on("pageerror", lambda e: erros.append((secao_atual[0], str(e)[:200])))
        pg.on(
            "console",
            lambda m: erros.append((secao_atual[0], "console: " + m.text[:160]))
            if m.type == "error" and "ERR_" not in m.text and "Failed to load" not in m.text
            else None,
        )
        # Sem internet de propósito: o Atlas tem que funcionar offline.
        pg.route("**/*wiki*", lambda r: r.abort())
        pg.goto(ARQUIVO.as_uri())
        pg.wait_for_timeout(1500)
        pg.evaluate(
            "()=>{window.speechSynthesis&&(window.speechSynthesis.speak=function(){});"
            "window.open=()=>null;HTMLAnchorElement.prototype.click=function(){}}"
        )

        duplicados = pg.evaluate(
            "()=>{const c={};document.querySelectorAll('[id]').forEach(e=>c[e.id]=(c[e.id]||0)+1);"
            "return Object.entries(c).filter(([k,v])=>v>1).map(([k])=>k)}"
        )
        for d in duplicados:
            erros.append(("estrutura", f"id duplicado: {d}"))

        secoes = pg.evaluate("()=>[...document.querySelectorAll('#atlasUxSelect option')].map(o=>o.value)")
        abrir = "v=>{const x=document.getElementById('atlasUxSelect');x.value=v;x.dispatchEvent(new Event('change'))}"
        for s in secoes:
            secao_atual[0] = s
            pg.evaluate(abrir, s)
            pg.wait_for_timeout(400)
            vista = pg.evaluate("()=>document.body.dataset.view")
            if vista != s:
                erros.append((s, f"seção não abriu (tela ficou em '{vista}')"))
                continue
            largura = pg.evaluate("()=>document.documentElement.scrollWidth")
            if largura > 410:
                erros.append((s, f"página mais larga que o celular ({largura}px)"))
            n = pg.evaluate(
                "v=>{const sec=document.getElementById(v);if(!sec)return 0;"
                "return [...sec.querySelectorAll('button')].filter(b=>b.offsetParent).length}",
                s,
            )
            for i in range(min(n, MAX_BOTOES_POR_SECAO)):
                pg.evaluate(
                    "([v,i,pular])=>{const sec=document.getElementById(v);if(!sec)return;"
                    "const bs=[...sec.querySelectorAll('button')].filter(b=>b.offsetParent);"
                    "if(bs[i]&&!new RegExp(pular,'i').test(bs[i].innerText))bs[i].click()}",
                    [s, i, PULAR_BOTOES],
                )
                pg.wait_for_timeout(60)
                if pg.evaluate("()=>document.body.dataset.view") != s:
                    pg.evaluate(abrir, s)
        nav.close()

    if not erros:
        print("OK — nenhum erro encontrado.")
        return 0
    print("ERROS ENCONTRADOS (seção, mensagem, vezes):")
    for (secao, msg), vezes in collections.Counter(erros).most_common():
        print(f"- [{secao}] {msg}  (x{vezes})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
