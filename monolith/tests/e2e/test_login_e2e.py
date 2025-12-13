# import re
# from playwright.sync_api import sync_playwright, expect

# def test_playwright():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=500)
#         page = browser.new_page()

#         page.goto("https://playwright.dev/")
#         expect(page).to_have_title(re.compile("Playwright"))
#         print("Teste do título concluído ✅")

#         page.goto("https://playwright.dev/")
#         page.get_by_role("link", name="Get started").click()
#         expect(page.get_by_role("heading", name="Installation")).to_be_visible()
#         print("Teste do link 'Get started' concluído ✅")

#         browser.close()