import xml.etree.ElementTree as ET

def parse_yml_to_meta(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    offers = root.findall(".//offer")
    items = []

    for offer in offers:
        quantity = offer.findtext("quantity_in_stock")
        available = offer.attrib.get("available", "true")

        if quantity == "0" or available.lower() == "false":
            availability = "out of stock"
        else:
            availability = "in stock"

        image_link = offer.findtext("picture")
        link = offer.findtext("url")

        # собираем описание заранее
        description_text = " ".join([param.text for param in offer.findall("param") if param.text]) or ""

        # определяем категорию по описанию
        fb_category = "204" if "колонка" in description_text.lower() else "207"

        # пропускаем товар, если нет и картинки, и ссылки
        if not image_link and not link:
            continue

        item = {
            "id": offer.attrib.get("id"),
            "title": offer.findtext("name") or "",
            "description": description_text,
            "price": offer.findtext("price"),
            "sale_price": offer.findtext("oldprice"),
            "availability": availability,
            "brand": offer.findtext("vendor"),
            "image_link": image_link,
            "link": link,
            "facebook_product_category": fb_category,
        }
        items.append(item)

    return items
