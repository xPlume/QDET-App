from text2props.text2props.constants import DIFFICULTY, DISCRIMINATION, FACILITY

"""
Defining the dictionary of the latent traits.
Assigning all attributes here allows us to need
only this function for all use-cases that are 
latent-trait specific
"""
def latent_trait_dictionary():
	
	latent_trait = {
		'difficulty': {
			"LATENT-TRAIT": DIFFICULTY,
			"attribute": 'question_difficulty',
			"query": 'question_difficulty__isnull',
		},
		'discrimination': {
			"LATENT-TRAIT": DISCRIMINATION,
			"attribute": 'question_discrimination',
			"query": 'question_discrimination__isnull',
		},
		'facility': {
			"LATENT-TRAIT": FACILITY,
			"attribute": 'question_facility',
			"query": 'question_facility__isnull',
		},
	}
	
	return latent_trait
#def