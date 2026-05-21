import flet as ft
import time

def main(page: ft.Page):
    page.title = "Todo App"
    page.bgcolor = "#0f0f23"
    page.padding = 0
    page.window_min_width = 350

    task_list = ft.Column(scroll="auto", expand=True, spacing=8)
    completed_count = ft.Text("0 completed", color="#6c63ff", size=12, weight="bold")
    total_count = ft.Text("0 tasks", color="#888888", size=12)

    def show_snack(msg, color="#6c63ff"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg, color="white"),
            bgcolor=color,
            duration=1500,
        )
        page.snack_bar.open = True
        page.update()

    def update_counts():
        done = sum(1 for c in task_list.controls if c.content.controls[0].value)
        total_count.value = f"{len(task_list.controls)} tasks"
        completed_count.value = f"{done} completed"
        page.update()

    def delete_task(e):
        card = e.control.data
        card.opacity = 0
        card.scale = ft.Scale(0.8)
        page.update()
        time.sleep(0.2)
        task_list.controls.remove(card)
        update_counts()
        show_snack("Task delete ho gaya!", "#e94560")

    def task_changed(e):
        update_counts()

    task_input = ft.TextField(
        hint_text="✨ Naya task likho...",
        hint_style=ft.TextStyle(color="#555577"),
        color="white",
        bgcolor="#1a1a3e",
        border_color="#6c63ff",
        border_radius=16,
        focused_border_color="#a78bfa",
        expand=True,
        height=52,
        text_size=15,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=14),
    )

    def add_task(e):
        if not task_input.value.strip():
            show_snack("Kuch likho pehle! ✍️", "#e94560")
            return

        task_text = task_input.value.strip()

        task_card = ft.Container(
            opacity=0,
            scale=ft.Scale(0.9),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    fill_color="#6c63ff",
                    check_color="white",
                    on_change=task_changed
                ),
                ft.Text(
                    task_text,
                    color="white",
                    size=15,
                    expand=True,
                    weight="w500",
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#e94560",
                    icon_size=20,
                    on_click=delete_task,
                    tooltip="Delete",
                )
            ]),
            bgcolor="#1a1a3e",
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border=ft.border.all(1, "#2a2a5e"),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#00000066",
                offset=ft.Offset(0, 4)
            ),
        )

        task_card.content.controls[2].data = task_card
        task_list.controls.append(task_card)
        task_input.value = ""
        update_counts()
        task_card.opacity = 1
        task_card.scale = ft.Scale(1)
        page.update()
        show_snack("Task add ho gaya! ✅", "#6c63ff")

    add_btn = ft.Container(
        content=ft.Icon(ft.icons.ADD, color="white", size=26),
        bgcolor="#6c63ff",
        border_radius=16,
        padding=ft.padding.all(13),
        on_click=add_task,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color="#6c63ff66",
            offset=ft.Offset(0, 4)
        ),
    )

    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.icons.TASK_ALT, color="white", size=28),
                    bgcolor="#6c63ff",
                    border_radius=12,
                    padding=ft.padding.all(8),
                ),
                ft.Column([
                    ft.Text("My Tasks", size=22, weight="bold", color="white"),
                    ft.Text("Aaj ka kaam", size=11, color="#888888"),
                ], spacing=0),
            ], spacing=12),
            ft.Divider(color="#2a2a5e", height=1),
            ft.Row([
                ft.Row([
                    ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="#6c63ff", size=14),
                    completed_count,
                ], spacing=4),
                ft.Row([
                    ft.Icon(ft.icons.LIST, color="#888888", size=14),
                    total_count,
                ], spacing=4),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=12),
        bgcolor="#13132e",
        padding=ft.padding.all(20),
        border=ft.border.only(bottom=ft.BorderSide(1, "#2a2a5e")),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color="#00000088",
            offset=ft.Offset(0, 4)
        ),
    )

    input_area = ft.Container(
        content=ft.Row([task_input, add_btn], spacing=10),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#0f0f23",
    )

    empty_state = ft.Container(
        content=ft.Column([
            ft.Text("🎯", size=50),
            ft.Text("Koi task nahi!", color="#555577", size=16, weight="bold"),
            ft.Text("Upar se task add karo", color="#333355", size=13),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        alignment=ft.alignment.center,
        expand=True,
    )

    page.add(
        header,
        input_area,
        ft.Divider(color="#2a2a5e", height=1),
        ft.Container(
            content=ft.Stack([
                empty_state,
                ft.Container(
                    content=task_list,
                    padding=ft.padding.all(16),
                    expand=True,
                )
            ]),
            expand=True,
        ),
    )

ft.app(target=main)