import hunspell
import sys

spellchecker = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.aff",
)

print (spellchecker.suggest(sys.argv[1]))
