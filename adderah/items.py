from dataclasses import dataclass, field
import w3lib.html


@dataclass
class Shipping:
    direction: str = ''
    method: str = ''
    duration: str = ''
    price: str = ''

    def __post_init__(self):

        self.direction = w3lib.html.remove_tags(self.direction).strip().strip('\n')
        self.method = w3lib.html.remove_tags(self.method).strip().strip('\n')
        self.duration = w3lib.html.remove_tags(self.duration).strip().strip('\n')
        self.price = float(
            w3lib.html.remove_tags(self.price).replace('ر.س', '').replace(',', '').strip('\t').strip()
        )


@dataclass
class Item:
    image_urls: list[str]
    images: list[str]
    shipping: list[Shipping]
    name: str = ''
    price: str = ''
    seller: str = ''
    in_stock: str = ''
    description: list[str] = field(default=list)
    category: str = ''
    subcategory: str = ''
    url: str = ''

    def __post_init__(self):

        self.name = self.name.strip().strip('\n')
        self.price = float(self.price.replace('ر.س', '').replace(',', '').strip('\t').strip())
        self.seller = self.seller.strip().strip('\n')
        self.in_stock = self.in_stock.strip().strip('\n')

        try:
            self.in_stock = int(self.in_stock)
        except:  # noqa: E722
            self.in_stock = 0
        
        self.category = self.category.strip().strip('\n')
        self.subcategory = self.subcategory.strip().strip('\n')

        self.description = " ".join([d.strip().strip('\n') for d in self.description])
        