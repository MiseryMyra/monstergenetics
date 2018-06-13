#module used for generating descriptions of monster species based on their average stats and population

def des_xp(xp):
    #returns a descriptor for a monster's experience value
    if xp >= 100000:
        return 'a god among mortals, simply beyond our understanding of nature'
    elif xp >= 50000:
        return 'the ultimate lifeform, peerless among monsters'
    elif xp >= 10000:
        return 'a truly supreme entity'
    elif xp >= 5000:
        return 'a marvelous being'
    elif xp >= 2500:
        return 'an extraordinary creation'
    elif xp >= 1000:
        return 'a superb monster'
    elif xp >= 750:
        return 'a prime fiend'
    elif xp >= 500:
        return 'a fearsome beast'
    elif xp >= 250:
        return 'a great creature'
    elif xp >= 100:
        return 'a peculiar animal'
    else:
        return 'an unremarkable critter'

def des_pw(pw):
    #returns a descriptor for a monster's power
    if pw >= 100:
        return 'with a mysterious force beyond comprehension'
    elif pw >= 75:
        return 'by obliterating its prey with a mere touch'
    elif pw >= 50:
        return 'by exhaling fire, igniting its victims'
    elif pw >= 40:
        return 'by bisecting its prey with a long bladed forelimb'
    elif pw >= 30:
        return 'by crushing its prey with its gargantuan jaws'
    elif pw >= 20:
        return 'by impaling its prey on its spear-like tail'
    elif pw >= 15:
        return 'with its fearsome spiked mandibles'
    elif pw >= 12:
        return 'with its numerous serrated teeth'
    elif pw >= 10:
        return 'with its gnarled horns'
    elif pw >= 8:
        return 'with its razor-like claws'
    elif pw >= 6:
        return 'with its venomous fangs'
    elif pw >= 4:
        return 'with its stinging tentacles'
    elif pw >= 2:
        return 'by swinging its limbs wildly'
    else:
        return 'by secreting a digestive enzyme'

def des_df(df):
    #returns a descriptor for a monster's defense
    if df >= 50:
        return 'radiates like the sun and is seemingly intangible'
    elif df >= 40:
        return 'is protected by a shimmering force field'
    elif df >= 30:
        return 'is entirely crystalline with the hardness of diamond'
    elif df >= 20:
        return 'is covered with thick armor-like plating'
    elif df >= 15:
        return 'is solid and rough like stone'
    elif df >= 12:
        return 'can retract entirely into a massive shell'
    elif df >= 10:
        return 'carries a dense shell on its back'
    elif df >= 8:
        return 'has a tough barbed exoskeleton'
    elif df >= 6:
        return 'is covered in large rough scales'
    elif df >= 5:
        return 'is covered in thick skin with bony plating'
    elif df >= 4:
        return 'is covered in smooth scales'
    elif df >= 3:
        return 'has a coat of feathers'
    elif df >= 2:
        return 'has a thick coat of fur'
    elif df >= 1:
        return 'has bare skin with some patches of fur'
    else:
        return 'is soft and jelly-like'

def des_dx(dx):
    #returns a descriptor for a monster's dexterity
    if dx >= 20:
        return 'harmoniously'
    elif dx >= 15:
        return 'elegantly'
    elif dx >= 12:
        return 'gracefully'
    elif dx >= 10:
        return 'nimbly'
    elif dx >= 8:
        return 'deliberately'
    elif dx >= 6:
        return 'clumsily'
    elif dx >= 4:
        return 'ineptly'
    elif dx >= 2:
        return 'erratically'
    else:
        return 'completely unpredictably'

def des_sp(sp):
    #returns a descriptor for a monster's speed
    if sp >= 50:
        return 'teleporting from location to location, as if by magic'
    elif sp >= 40:
        return 'blasting off with sudden massive bursts of speed'
    elif sp >= 30:
        return 'flying with its great majestic wings'
    elif sp >= 20:
        return 'hovering with its short rapidly flapping wings'
    elif sp >= 15:
        return 'sprinting with its hindlimbs'
    elif sp >= 12:
        return 'running with its forelimbs and hindlimbs'
    elif sp >= 10:
        return 'walking with its forelimbs'
    elif sp >= 8:
        return 'taking short hops with its hindlimbs'
    elif sp >= 6:
        return 'crawling low to the ground'
    elif sp >= 5:
        return 'sliding around on its tentacles'
    elif sp >= 4:
        return 'dragging itself by its forelimbs'
    elif sp >= 3:
        return 'rolling around on the ground'
    elif sp >= 2:
        return 'undulating its body against the ground'
    elif sp >= 1:
        return 'slithering on its slimy underside'
    else:
        return 'slowly shifting its roots in the ground'

def des_pr(pr):
    #returns a descriptor for a monster's perception
    if pr >= 20:
        return 'seemingly telepathically with no visible external sensory organs'
    elif pr >= 15:
        return 'with a single eye on its forehead that is very sensitive to infrared radiation'
    elif pr >= 12:
        return 'with a large pair of ears used for echolocation'
    elif pr >= 10:
        return 'with a sensitive nose on a long snout'
    elif pr >= 8:
        return 'with a pair of large compound eyes'
    elif pr >= 6:
        return 'by collecting odors with its long forked tongue'
    elif pr >= 4:
        return 'with a pair of short antennae on its head'
    elif pr >= 2:
        return 'with a series of fine hairs on its body'
    else:
        return 'by groping at its surroundings with its forelimbs'

def des_hp(hp):
    #returns a descriptor for a monster's hit points
    if hp >= 200:
        return 'is absolutely massive beyond comprehension'
    elif hp >= 150:
        return 'has a gargantuan body that towers over almost all living things'
    elif hp >= 100:
        return 'has an enormous body larger than a standard dwelling'
    elif hp >= 75:
        return 'is a giant among monsters'
    elif hp >= 50:
        return 'has a very large and sturdy body'
    elif hp >= 40:
        return 'has a fairly tall and hefty body'
    elif hp >= 30:
        return 'stands no taller than a person'
    elif hp >= 20:
        return 'has a short lean body'
    elif hp >= 10:
        return 'has a small slim body'
    elif hp >= 5:
        return 'has a tiny frail body'
    else:
        return 'has a minuscule delicate body'

def des_pop(pop):
    #returns a descriptor for a monster's population
    if pop >= 100:
        return 'is completely ubiquitous and has taken over its environment'
    elif pop >= 75:
        return 'is one of the dominant life forms in its environment'
    elif pop >= 50:
        return 'has a considerably large population'
    elif pop >= 40:
        return 'is very common in its environment'
    elif pop >= 30:
        return 'is found throughout its environment'
    elif pop >= 20:
        return 'has a modest but stable population'
    elif pop >= 10:
        return 'is rare in its environment'
    elif pop >= 5:
        return 'is endangered'
    elif pop >= 2:
        return 'is critically endangered'
    else:
        return 'is the last of its kind'
        
def des_sc(sc):
    #returns a descriptor for a monster's social stat
    if sc >= 20:
        return 'forms a complex social structure with other members of its own species built on teamwork and mutual care'
    elif sc >= 15:
        return 'prefers to live in large groups with many other members of its own species'
    elif sc >= 12:
        return 'forms communities within its own species'
    elif sc >= 10:
        return 'seems to take care of other members of its own species'
    elif sc >= 8:
        return 'is a somewhat social species'
    elif sc >= 6:
        return 'has limited interactions with other members of its own species'
    elif sc >= 4:
        return 'mostly ignores other members of its own species'
    elif sc >= 2:
        return 'does not enjoy being with members of its own species'
    else:
        return 'prefers to live in solitude'
        
def des_ag(ag):
    #returns a descriptor for a monster's aggression
    if ag >= 20:
        return 'lives an enraged life full of fury and conflict until the bitter end'
    elif ag >= 15:
        return 'is extremely hostile and attacks at a moment\'s notice'
    elif ag >= 12:
        return 'is antagonistic toward most living things'
    elif ag >= 10:
        return 'is quite aggressive, even with members of its own species'
    elif ag >= 7:
        return 'is somewhat aggressive, but only toward other species'
    elif ag >= 5:
        return 'seems calm, but it fights if it must'
    elif ag >= 3:
        return 'is a somewhat meek creature that tries not to fight'
    elif ag >= 1:
        return 'is a very docile animal'
    else:
        return 'avoids conflict at all costs'

def des_name(name):
    #returns a semi-random descriptor based on a monster's name
    features = ['its striped exterior', 'a ribbed crest on its head', 'its long flowing mane', 'a hooked beak on its face', 'its forked prehensile tail', 'its transparent exterior', 'its spotted exterior', 'its long tusks', 'its asymmetric body', 'a disproportionately large claw', 'its reflective exterior', 'its spindly extra limbs', 'its complex mouthparts', 'a star-shaped mark on its back', 'its numerous slime-tipped filaments', 'its gaping maw', 'its short blunted antlers', 'its twisted fingernails', 'its bulging cheeks', 'its bushy brow', 'a false face on its backside', 'its numerous fins', 'a hump on its back', 'its flowering branches', 'its coiled proboscis', 'a strange moss growing on its exterior', 'its long whiskers', 'its broad and long front teeth', 'a series of glowing spots on its body', 'its brightly colored throat', 'a small pair of extra limbs on its face', 'its rotationally symmetric body', 'its ability to curl into a ball', 'its ability to shed its exterior', 'a series of small pouches in its back', 'its asymmetric face', 'its bristled forelimbs', 'a long bony finger on one forelimb', 'its translucent skin', 'its strainer-lined mouth', 'its coiled body']
    index = sum(bytearray(name)) % len(features)

    return features[index]

def generate_description(name, pop, stats):
    #makes a fanciful description of a monster based on its stats and population
    #pop = population[name]

    #extinct creature
    if pop < 1:
        description = 'The ' + name + ' is an extinct creature which, according to legend, was notable for ' + des_name(name) + '. Otherwise, its appearance and lifestyle are a mystery that has been lost to time.'
    
    else:
        #stats = total_monster_stats(name)
        xp = stats['xp']['avg']
        pw = stats['pw']['avg']
        df = stats['df']['avg']
        dx = stats['dx']['avg']
        sp = stats['sp']['avg']
        pr = stats['pr']['avg']
        hp = stats['hp']['avg']
        sc = stats['sc']['avg']
        ag = stats['ag']['avg']
        
        description = 'The ' + name + ' is ' + des_xp(xp) + '. Its body ' + des_df(df) + ', and it attacks ' + des_pw(pw) + '. It moves by ' + des_dx(dx) + ' ' + des_sp(sp) + ', and it senses ' + des_pr(pr) + '. Its most distinctive feature is ' + des_name(name) + '. It ' + des_hp(hp) + ', and it ' + des_pop(pop) + '.\n\nBehaviorally, the ' + name + ' ' + des_sc(sc) + ', and it ' + des_ag(ag) + '.'

    description = description + '\n\nPress any key to exit.'

    return description
