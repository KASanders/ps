from flask import Flask

from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection, CtsTextInventoryMetadata
from MyCapytain.resolvers.utils import CollectionDispatcher


from capitains_nautilus.cts.resolver import NautilusCTSResolver
from capitains_nautilus.flask_ext import FlaskNautilus
from flask_nemo.chunker import level_grouper
from flask_nemo import Nemo

def meadow_chunker(text, getreffs):
    # We build a list of the number
    chapters = []
    for chapter_number in range(0, 81):  # Range in Python stops before its end limit
        chapters.append(
            (  # Tuple are written with an () in python
                str(chapter_number),                   # First the reference for the URI as string
                "Pratum Spirituale "+ str(chapter_number)  # Then the readable format for humans
            )
        )
    return chapters

# Setting up the collections

general_collection = CtsTextInventoryCollection()

greek_texts = CtsTextInventoryMetadata("greek_texts", parent=general_collection)
greek_texts.set_label("Greek Texts", "eng")



organizer = CollectionDispatcher(general_collection, default_inventory_name="id:misc")

@organizer.inventory("greek_texts")
def organize_my_meadow(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:greekLit"):
        return True
    return False


flask_app = Flask("Flask Application for Nemo")
resolver = NautilusCTSResolver(["corpora/meadow"], dispatcher=organizer)
resolver.parse()

nautilus_api = FlaskNautilus(prefix="/api", app=flask_app, resolver=resolver)

nemo = Nemo(
    name="InstanceNemo",
    app=flask_app,
    resolver=resolver,
    base_url="",
    css=["assets/css/theme.css"],
    js=["assets/js/alpheios.js"],
    statics=["assets/images/logo.jpg"],
    transform={"default": "components/main.xsl"},
    templates={"main": "templates/main"},
    chunker={"urn:cts:greekLit:tlg2856.tlg001.1st1K-grc1": meadow_chunker}
)


if __name__ == "__main__":
    flask_app.run(debug=True)
