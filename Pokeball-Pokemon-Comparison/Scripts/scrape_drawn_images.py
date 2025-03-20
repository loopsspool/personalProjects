import globals
from scrape_image_tools import get_img_from_string

# TODO: Should probably also have a quick way to download drawn regional variants since they're likely to introduce more at some point

# TODO: Where is this actually used? Maybe I got rid of it since I cleared them all?
def search_for_drawn_forms(pokemon, save_name, thumb):
    # Custom type forms
    # Pikachu Cosplay & Caps
    get_img_from_string(thumb, "^\d\d\dPikachu-Alola.png", drawn_save_path + save_name + "-Cap-Alola")
    get_img_from_string(thumb, "^\d\d\dPikachu-Hoenn.png", drawn_save_path + save_name + "-Cap-Hoenn")
    get_img_from_string(thumb, "^\d\d\dPikachu-Kalos.png", drawn_save_path + save_name + "-Cap-Kalos")
    get_img_from_string(thumb, "^\d\d\dPikachu-Original.png", drawn_save_path + save_name + "-Cap-Original")
    get_img_from_string(thumb, "^\d\d\dPikachu-Partner.png", drawn_save_path + save_name + "-Cap-Partner")
    get_img_from_string(thumb, "^\d\d\dPikachu-Sinnoh.png", drawn_save_path + save_name + "-Cap-Sinnoh")
    get_img_from_string(thumb, "^\d\d\dPikachu-Unova.png", drawn_save_path + save_name + "-Cap-Unova")
    get_img_from_string(thumb, "^\d\d\dPikachu-World.png", drawn_save_path + save_name + "-Cap-World")
    get_img_from_string(thumb, "^\d\d\dPikachu-Belle.png", drawn_save_path + save_name + "-Cosplay-Belle")
    get_img_from_string(thumb, "^\d\d\dPikachu-Libre.png", drawn_save_path + save_name + "-Cosplay-Libre")
    get_img_from_string(thumb, "^\d\d\dPikachu-PhD.png", drawn_save_path + save_name + "-Cosplay-PhD")
    get_img_from_string(thumb, "^\d\d\dPikachu-Pop Star.png", drawn_save_path + save_name + "-Cosplay-Pop_Star")
    get_img_from_string(thumb, "^\d\d\dPikachu-Rock Star.png", drawn_save_path + save_name + "-Cosplay-Rock_Star")

    # Spiky-eared Pichu
    get_img_from_string(thumb, "Spiky-eared Pichu DP 1", drawn_save_path + save_name + "-Spiky_Eared")

    # Unown Characters
    if pokemon.name == "Unown":
        # Only drawn forms are dream versions
        if thumb.img["alt"].endswith("Dream.png"):
            # Get form
            form = thumb.img["alt"].split(" ")[1]
            if form == "Exclamation":
                form = "!"    
            if form == "Question":
                form = "Qmark"
            form = "-" + form
            get_img_from_string(thumb, "^\d\d\dUnown [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Castform Weathers
    get_img_from_string(thumb, "^\d\d\dCastform-Rainy.png", drawn_save_path + save_name + "-Rainy")
    get_img_from_string(thumb, "^\d\d\dCastform-Snowy.png", drawn_save_path + save_name + "-Snowy")
    get_img_from_string(thumb, "^\d\d\dCastform-Sunny.png", drawn_save_path + save_name + "-Sunny")

    # Primal Kyogre & Groudon
    get_img_from_string(thumb, "^\d\d\dKyogre-Primal 2.png", drawn_save_path + save_name + "-Primal")
    get_img_from_string(thumb, "^\d\d\dGroudon-Primal.png", drawn_save_path + save_name + "-Primal")

    # Deoxys
    get_img_from_string(thumb, "^\d\d\dDeoxys-Attack.png", drawn_save_path + save_name + "-Attack")
    get_img_from_string(thumb, "^\d\d\dDeoxys-Defense.png", drawn_save_path + save_name + "-Defense")
    get_img_from_string(thumb, "^\d\d\dDeoxys-Speed.png", drawn_save_path + save_name + "-Speed")

    # Burmy & Wormadam Cloaks
    get_img_from_string(thumb, "^\d\d\dBurmy-Plant.png", drawn_save_path + save_name + "-Plant")
    get_img_from_string(thumb, "^\d\d\dBurmy-Sandy.png", drawn_save_path + save_name + "-Sandy")
    get_img_from_string(thumb, "^\d\d\dBurmy-Trash.png", drawn_save_path + save_name + "-Trash")
    get_img_from_string(thumb, "^\d\d\dWormadam-Plant.png", drawn_save_path + save_name + "-Plant")
    get_img_from_string(thumb, "^\d\d\dWormadam-Sandy.png", drawn_save_path + save_name + "-Sandy")
    get_img_from_string(thumb, "^\d\d\dWormadam-Trash.png", drawn_save_path + save_name + "-Trash")

    # Cherrim
    # NOTE: No default image, only overcast and sunny
    get_img_from_string(thumb, "^\d\d\dCherrim-Overcast.png", drawn_save_path + save_name + "-Overcast")
    get_img_from_string(thumb, "^\d\d\dCherrim-Sunny.png", drawn_save_path + save_name + "-Sunshine")

    # Shellos & Gastrodon East/West
    # NOTE: No default image
    get_img_from_string(thumb, "^\d\d\dShellos-East.png", drawn_save_path + save_name + "-East")
    get_img_from_string(thumb, "^\d\d\dShellos-West.png", drawn_save_path + save_name + "-West")
    get_img_from_string(thumb, "^\d\d\dGastrodon-East.png", drawn_save_path + save_name + "-East")
    get_img_from_string(thumb, "^\d\d\dGastrodon-West.png", drawn_save_path + save_name + "-West")

    # Rotom Appliances
    get_img_from_string(thumb, "^\d\d\dRotom-Fan.png", drawn_save_path + save_name + "-Fan")
    get_img_from_string(thumb, "^\d\d\dRotom-Frost.png", drawn_save_path + save_name + "-Frost")
    get_img_from_string(thumb, "^\d\d\dRotom-Heat.png", drawn_save_path + save_name + "-Heat")
    get_img_from_string(thumb, "^\d\d\dRotom-Mow.png", drawn_save_path + save_name + "-Mow")
    get_img_from_string(thumb, "^\d\d\dRotom-Wash.png", drawn_save_path + save_name + "-Wash")

    # Giratina
    # NOTE: No default image
    get_img_from_string(thumb, "^\d\d\dGiratina-Altered.png", drawn_save_path + save_name + "-Altered")
    get_img_from_string(thumb, "^\d\d\dGiratina-Origin.png", drawn_save_path + save_name + "-Origin")

    # Shaymin
    # NOTE: No default image
    get_img_from_string(thumb, "^\d\d\dShaymin-Land.png", drawn_save_path + save_name + "-Land")
    get_img_from_string(thumb, "^\d\d\dShaymin-Sky.png", drawn_save_path + save_name + "-Sky")

    # Arceus Types
    # Only drawn forms are dream versions
    if pokemon.name == "Arceus":
        if thumb.img["alt"].endswith("Dream.png"):
            # Get form
            form = thumb.img["alt"].split(" ")[1]
            form = "-" + form
            get_img_from_string(thumb, "^\d\d\dArceus [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Basculin Stripes
    get_img_from_string(thumb, "^\d\d\dBasculin-Red-Striped_XY_Anime.png", drawn_save_path + save_name + "-Red_Striped")
    get_img_from_string(thumb, "^\d\d\dBasculin-Blue-Striped_BW_Anime.png", drawn_save_path + save_name + "-Blue_Striped")

    # Darmanitan Modes
    get_img_from_string(thumb, "^\d\d\dDarmanitan.png", drawn_save_path + save_name + "-Standard")
    get_img_from_string(thumb, "^\d\d\dDarmanitan-Galar.png", drawn_save_path + save_name + "-Region-Galar-Standard")
    get_img_from_string(thumb, "^\d\d\dDarmanitan-Zen.png", drawn_save_path + save_name + "-Zen")
    get_img_from_string(thumb, "^\d\d\dDarmanitan-Galar-Zen.png", drawn_save_path + save_name + "-Region-Galar-Zen")

    # Deerling & Sawsbuck Seasons
    # NOTE: No default image
    get_img_from_string(thumb, "^\d\d\dDeerling-Autumn.png", drawn_save_path + save_name + "-Autumn")
    get_img_from_string(thumb, "^\d\d\dDeerling-Spring.png", drawn_save_path + save_name + "-Spring")
    get_img_from_string(thumb, "^\d\d\dDeerling-Summer.png", drawn_save_path + save_name + "-Summer")
    get_img_from_string(thumb, "^\d\d\dDeerling-Winter.png", drawn_save_path + save_name + "-Winter")
    get_img_from_string(thumb, "^\d\d\dSawsbuck-Autumn.png", drawn_save_path + save_name + "-Autumn")
    get_img_from_string(thumb, "^\d\d\dSawsbuck-Spring.png", drawn_save_path + save_name + "-Spring")
    get_img_from_string(thumb, "^\d\d\dSawsbuck-Summer.png", drawn_save_path + save_name + "-Summer")
    get_img_from_string(thumb, "^\d\d\dSawsbuck-Winter.png", drawn_save_path + save_name + "-Winter")

    # Forces of nature forms
    get_img_from_string(thumb, "^\d\d\dTornadus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(thumb, "^\d\d\dTornadus-Therian.png", drawn_save_path + save_name + "-Therian")
    get_img_from_string(thumb, "^\d\d\dThundurus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(thumb, "^\d\d\dThundurus-Therian.png", drawn_save_path + save_name + "-Therian")
    get_img_from_string(thumb, "^\d\d\dLandorus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(thumb, "^\d\d\dLandorus-Therian.png", drawn_save_path + save_name + "-Therian")

    # Kyurem Fusions
    get_img_from_string(thumb, "^\d\d\dKyurem-Black.png", drawn_save_path + save_name + "-Black")
    get_img_from_string(thumb, "^\d\d\dKyurem-Black2.png", drawn_save_path + save_name + "-Black_Overdrive")
    get_img_from_string(thumb, "^\d\d\dKyurem-White.png", drawn_save_path + save_name + "-White")
    get_img_from_string(thumb, "^\d\d\dKyurem-White2.png", drawn_save_path + save_name + "-White_Overdrive")
    
    # Keldeo
    get_img_from_string(thumb, "^\d\d\dKeldeo.png", drawn_save_path + save_name + "-Ordinary")
    get_img_from_string(thumb, "^\d\d\dKeldeo-Resolute.png", drawn_save_path + save_name + "-Resolute")

    # Meloetta
    get_img_from_string(thumb, "^\d\d\dMeloetta.png", drawn_save_path + save_name + "-Aria")
    get_img_from_string(thumb, "^\d\d\dMeloetta-Pirouette.png", drawn_save_path + save_name + "-Pirouette")

    # Genesect
    # Only drawn forms are dream versions
    if pokemon.name == "Genesect":
        if thumb.img["alt"].endswith("Dream.png"):
            # Get form
            form = thumb.img["alt"].split(" ")[1]
            if form == "B":
                form = "Burn_Drive"
            if form == "C":
                form = "Chill_Drive"
            if form == "D":
                form = "Douse_Drive"
            if form == "S":
                form = "Shock_Drive"
            form = "-" + form
            get_img_from_string(thumb, "^\d\d\dGenesect [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Ash Greninja
    get_img_from_string(thumb, "^\d\d\dGreninja-Ash.png", drawn_save_path + save_name + "-Ash")

    # Vivillon Patterns
    get_img_from_string(thumb, "^\d\d\dVivillon-Archipelago.png", drawn_save_path + save_name + "-Archipelago")
    get_img_from_string(thumb, "^\d\d\dVivillon-Continental.png", drawn_save_path + save_name + "-Continental")
    get_img_from_string(thumb, "^\d\d\dVivillon-Elegant.png", drawn_save_path + save_name + "-Elegant")
    get_img_from_string(thumb, "^\d\d\dVivillon-Fancy.png", drawn_save_path + save_name + "-Fancy")
    get_img_from_string(thumb, "^\d\d\dVivillon-Garden.png", drawn_save_path + save_name + "-Garden")
    get_img_from_string(thumb, "^\d\d\dVivillon-High Plains.png", drawn_save_path + save_name + "-High_Plains")
    get_img_from_string(thumb, "^\d\d\dVivillon-Icy Snow.png", drawn_save_path + save_name + "-Icy_Snow")
    get_img_from_string(thumb, "^\d\d\dVivillon-Jungle.png", drawn_save_path + save_name + "-Jungle")
    get_img_from_string(thumb, "^\d\d\dVivillon-Marine.png", drawn_save_path + save_name + "-Marine")
    get_img_from_string(thumb, "^\d\d\dVivillon-Meadow.png", drawn_save_path + save_name + "-Meadow")
    get_img_from_string(thumb, "^\d\d\dVivillon-Modern.png", drawn_save_path + save_name + "-Modern")
    get_img_from_string(thumb, "^\d\d\dVivillon-Monsoon.png", drawn_save_path + save_name + "-Monsoon")
    get_img_from_string(thumb, "^\d\d\dVivillon-Ocean.png", drawn_save_path + save_name + "-Ocean")
    get_img_from_string(thumb, "^\d\d\dVivillon-Poké Ball.png", drawn_save_path + save_name + "-Poke_Ball")
    get_img_from_string(thumb, "^\d\d\dVivillon-Polar.png", drawn_save_path + save_name + "-Polar")
    get_img_from_string(thumb, "^\d\d\dVivillon-River.png", drawn_save_path + save_name + "-River")
    get_img_from_string(thumb, "^\d\d\dVivillon-Sandstorm.png", drawn_save_path + save_name + "-Sandstorm")
    get_img_from_string(thumb, "^\d\d\dVivillon-Savanna.png", drawn_save_path + save_name + "-Savanna")
    get_img_from_string(thumb, "^\d\d\dVivillon-Sun.png", drawn_save_path + save_name + "-Sun")
    get_img_from_string(thumb, "^\d\d\dVivillon-Tundra.png", drawn_save_path + save_name + "-Tundra")


    # Flabebe, Floette, and Florges colors
    get_img_from_string(thumb, "^\d\d\dFlabébé Blue Flower XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(thumb, "^\d\d\dFlabébé Orange Flower XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(thumb, "^\d\d\dFlabébé Red Flower XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(thumb, "^\d\d\dFlabébé White Flower XY anime.png", drawn_save_path + save_name + "-White")
    get_img_from_string(thumb, "^\d\d\dFlabébé Yellow Flower XY anime.png", drawn_save_path + save_name + "-Yellow")
    get_img_from_string(thumb, "^\d\d\dFloette-Blue XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(thumb, "^\d\d\dFloette-Orange XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(thumb, "^\d\d\dFloette-Red XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(thumb, "^\d\d\dFloette-Yellow XY anime.png", drawn_save_path + save_name + "-Yellow")
    #get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    get_img_from_string(thumb, "^\d\d\dFlorges Blue Flower XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(thumb, "^\d\d\dFlorges Orange Flower XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(thumb, "^\d\d\dFlorges Red Flower XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(thumb, "^\d\d\dFlorges White Flower XY anime.png", drawn_save_path + save_name + "-White")
    get_img_from_string(thumb, "^\d\d\dFlorges Yellow Flower XY anime.png", drawn_save_path + save_name + "-Yellow")

    # Furfrou Trims
    get_img_from_string(thumb, "^\d\d\dFurfrou-Diamond.png", drawn_save_path + save_name + "-Diamond_Trim")
    get_img_from_string(thumb, "^\d\d\dFurfrou-Heart.png", drawn_save_path + save_name + "-Heart_Trim")
    get_img_from_string(thumb, "^\d\d\dFurfrou-Star.png", drawn_save_path + save_name + "-Star_Trim")
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Aegislash
    get_img_from_string(thumb, "^\d\d\dAegislash-Blade.png", drawn_save_path + save_name + "-Blade")
    get_img_from_string(thumb, "^\d\d\dAegislash-Shield.png", drawn_save_path + save_name + "-Shield")

    # Pumpkaboo and Gourgeist Sizes
    # if "Pumpkaboo" == split_name or "Gourgeist" == split_name:
    #     # Average sizes have no indication in filename on this website
    #     form = " 1Average Size"
    # else:
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Xerneas
    # if "Xerneas" == split_name:
    #     form = " Active"
    # else:
    #     get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Zygarde
    get_img_from_string(thumb, "^\d\d\dZygarde.png", drawn_save_path + save_name + "-50%")
    get_img_from_string(thumb, "^\d\d\dZygarde-10Percent.png", drawn_save_path + save_name + "-10%")
    get_img_from_string(thumb, "^\d\d\dZygarde-Complete.png", drawn_save_path + save_name + "-Complete")


    # Hoopa
    get_img_from_string(thumb, "^\d\d\dHoopa.png", drawn_save_path + save_name + "-Confined")
    get_img_from_string(thumb, "^\d\d\dHoopa-Unbound.png", drawn_save_path + save_name + "-Unbound")


    # Oricorio
    # NOTE: No default
    get_img_from_string(thumb, "^\d\d\dOricorio-Baile.png", drawn_save_path + save_name + "-Baile")
    get_img_from_string(thumb, "^\d\d\dOricorio-Pa'u.png", drawn_save_path + save_name + "-Pa'u")
    get_img_from_string(thumb, "^\d\d\dOricorio-Pom-Pom.png", drawn_save_path + save_name + "-Pom_Pom")
    get_img_from_string(thumb, "^\d\d\dOricorio-Sensu.png", drawn_save_path + save_name + "-Sensu")

    # Lycanroc
    get_img_from_string(thumb, "^\d\d\dLycanroc.png", drawn_save_path + save_name + "-Midday")
    get_img_from_string(thumb, "^\d\d\dLycanroc-Dusk.png", drawn_save_path + save_name + "-Dusk")
    get_img_from_string(thumb, "^\d\d\dLycanroc-Midnight.png", drawn_save_path + save_name + "-Midnight")

    # Wishiwashi
    # NOTE: No default
    get_img_from_string(thumb, "^\d\d\dWishiwashi-Solo.png", drawn_save_path + save_name + "-Solo")
    get_img_from_string(thumb, "^\d\d\dWishiwashi-School.png", drawn_save_path + save_name + "-School")

    # Silvally Types
    # Only drawn forms are dream versions
    if pokemon.name == "Silvally":
        if thumb.img["alt"].endswith("Dream.png"):
            # Get form
            form = thumb.img["alt"].split(" ")[1]
            form = "-" + form
            get_img_from_string(thumb, "^\d\d\dSilvally [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Minior
    get_img_from_string(thumb, "^\d\d\dMinior.png", drawn_save_path + save_name + "-Meteor")
    get_img_from_string(thumb, "^\d\d\dMinior-Core.png", drawn_save_path + save_name + "-Red_Core")
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )
    # # Shiny cores all the same color?
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Mimikyu
    get_img_from_string(thumb, "^\d\d\dMimikyu.png", drawn_save_path + save_name + "-Disguised")
    get_img_from_string(thumb, "^\d\d\dMimikyu Busted Dream.png", drawn_save_path + save_name + "-Busted")

    # Solgaleo
    get_img_from_string(thumb, "^\d\d\dSolgaleo-RadiantSunPhase.png", drawn_save_path + save_name + "-Radiant_Sun")

    # Lunala
    get_img_from_string(thumb, "^\d\d\dLunala-FullMoonPhase.png", drawn_save_path + save_name + "-Full_Moon")

    # Necrozma
    get_img_from_string(thumb, "^\d\d\dNecrozma-Dawn Wings.png", drawn_save_path + save_name + "-Dawn_Wings")
    get_img_from_string(thumb, "^\d\d\dNecrozma-Dusk Mane.png", drawn_save_path + save_name + "-Dusk_Mane")
    get_img_from_string(thumb, "^\d\d\dNecrozma-Ultra.png", drawn_save_path + save_name + "-Ultra")

    # Magearna
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Marshadow
    get_img_from_string(thumb, "^\d\d\dMarshadow-Alt.png", drawn_save_path + save_name + "-Zenith")

    # Cramorant
    get_img_from_string(thumb, "^\d\d\dCramorant-Gorging.png", drawn_save_path + save_name + "-Gorging")
    get_img_from_string(thumb, "^\d\d\dCramorant-Gulping.png", drawn_save_path + save_name + "-Gulping")

    # Toxtricity
    get_img_from_string(thumb, "^\d\d\dToxtricity-Amped.png", drawn_save_path + save_name + "-Amped")
    get_img_from_string(thumb, "^\d\d\dToxtricity-Low Key.png", drawn_save_path + save_name + "-Low_Key")

    # Alcremie Creams & Sweets
    # Default Alcremie is Vanilla Cream-Strawberry Sweet
    if pokemon.name == "Alcremie":
        # Space after excludes gigantamax img
        if re.search("^869Alcremie-[a-zA-Z]+ ", thumb.img["alt"]):
            # Getting largest image for Alcremie
            img_url = get_largest_png(thumb)
            # Splits by directory
            img_url = img_url.split("/")
            # Gets last string in sequence (the filename)
            img_url = img_url[len(img_url) - 1]
            # Splits by hyphen to get cream and sweet
            img_url = img_url.split("-")
            cream = "-" + img_url[1]
            sweet = "-" + img_url[2].replace(".png", "_Sweet")
            form = cream + sweet
            get_img_from_string(thumb, "^869Alcremie-[a-zA-Z]+ ", drawn_save_path + save_name + form)

    # Eiscue
    # NOTE: No default
    get_img_from_string(thumb, "^\d\d\dEiscue-Ice.png", drawn_save_path + save_name + "-Ice_Face")
    get_img_from_string(thumb, "^\d\d\dEiscue-Noice.png", drawn_save_path + save_name + "-Noice_Face")

    # Morpeko
    get_img_from_string(thumb, "^\d\d\dMorpeko-Full.png", drawn_save_path + save_name + "-Full")
    get_img_from_string(thumb, "^\d\d\dMorpeko-Hangry.png", drawn_save_path + save_name + "-Hangry")


    # Zacian and Zamazenta
    get_img_from_string(thumb, "^\d\d\dZacian.png", drawn_save_path + save_name + "-Crowned_Sword")
    get_img_from_string(thumb, "^\d\d\dZacian-Hero.png", drawn_save_path + save_name + "-Hero_of_Many_Battles")
    get_img_from_string(thumb, "^\d\d\dZamazenta.png", drawn_save_path + save_name + "-Crowned_Shield")
    get_img_from_string(thumb, "^\d\d\dZamazenta-Hero.png", drawn_save_path + save_name + "-Hero_of_Many_Battles")

    # Eternatus Eternamax
    # get_img_from_string(thumb, "^\d\d\d.png", drawn_save_path + save_name + )

    # Urshifu
    get_img_from_string(thumb, "^\d\d\dUrshifu-Gigantamax Rapid Strike.png", drawn_save_path + save_name + "Gigantamax-Rapid_Strike")
    get_img_from_string(thumb, "^\d\d\dUrshifu-Gigantamax Single Strike.png", drawn_save_path + save_name + "Gigantamax-Single_Strike")
    get_img_from_string(thumb, "^\d\d\dUrshifu-Rapid Strike.png", drawn_save_path + save_name + "-Rapid_Strike")
    get_img_from_string(thumb, "^\d\d\dUrshifu-Single Strike.png", drawn_save_path + save_name + "-Single_Strike")


    # Zarude
    get_img_from_string(thumb, "^\d\d\dZarude-Dada JN anime.png", drawn_save_path + save_name + "-Dada")

    # Calyrex Ridings
    get_img_from_string(thumb, "^\d\d\dCalyrex-Ice Rider.png", drawn_save_path + save_name + "-Ice_Rider")
    get_img_from_string(thumb, "^\d\d\dCalyrex-Shadow Rider.png", drawn_save_path + save_name + "-Shadow_Rider")

    # Zekrom Overdrive
    get_img_from_string(thumb, "^\d\d\dZekrom-Activated.png", drawn_save_path + save_name + "-Overdrive")
    # Reshiram Overdrive
    get_img_from_string(thumb, "^\d\d\dReshiram-Activated.png", drawn_save_path + save_name + "-Overdrive")

# TODO: Pokemon with hyphen, spaces, or numbers not downloading bc of regex
    # Just add a special character/whitespace 0 or more occurances flag
def get_drawn_images(pokemon, thumb):
    # DRAWN IMAGES
    # Drawn standard

    save_name = pokemon.number + " " + pokemon.name
    if pokemon.name == "Type: Null":
        save_name = pokemon.number + " Type Null"
    # Done this way so certain images that just have characters after the pokemon number don't match
        # Don't have to do this with the others because the hyphen denoters prevent the possibility
    pokemon_name_len = len(pokemon.name)
    get_img_from_string(thumb, "^\d\d\d[a-zA-Z]{" + str(pokemon_name_len) + "}.png", drawn_save_path + save_name)
    # Drawn Mega
    if pokemon.has_mega:
        if pokemon.name == "Charizard" or pokemon.name == "Mewtwo":
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Mega X.png", drawn_save_path + save_name + "-Mega_X")
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Mega Y.png", drawn_save_path + save_name + "-Mega_Y")
        else:
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Mega.png", drawn_save_path + save_name + "-Mega")
    # Gigantamax
    if pokemon.has_giganta:
        get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Gigantamax.png", drawn_save_path + save_name + "-Gigantamax")
    # Regional forms
    if pokemon.reg_forms != "":
        if "," in pokemon.reg_forms:
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Alola.png", drawn_save_path + save_name + "-Region-Alola")
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-Galar.png", drawn_save_path + save_name + "-Region-Galar")
        else:
            get_img_from_string(thumb, "^\d\d\d[a-zA-Z]+-" + pokemon.reg_forms + ".png", drawn_save_path + save_name + "-Region-" + pokemon.reg_forms)
    # Other forms
    if pokemon.has_misc_forms or pokemon.has_type_forms:
        search_for_drawn_forms(pokemon, save_name, thumb)