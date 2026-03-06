import flet as ft
from app.views.producto import producto_view

def main(page: ft.Page):
    page.title = "Flet App"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(producto_view(page))

if __name__ == "__main__":
    ft.run(main)