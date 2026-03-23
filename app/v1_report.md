# 📊 Rapport d’évaluation du modèle QA

## 1. Contexte

Le modèle utilisé est un modèle de Question Answering basé sur DistilBERT, avec une limite de 384 tokens.

## 2. Observation

La majorité des questions n’ont pas obtenu de réponse correcte :

- réponses absentes
- réponses incorrectes ou incomplètes

## 3. Analyse

### Modèle extractif

Le modèle est extractif :

- il extrait des réponses du texte
- il ne génère pas de nouvelles réponses

➡️ Problème :

- si la réponse n’est pas clairement présente dans le texte, le modèle échoue
- difficulté avec les questions de compréhension ou de raisonnement

### Limite de tokens

- contexte limité à 384 tokens
- possible perte d’informations importantes
- difficulté avec les textes longs

### Limite du modèle

DistilBERT est une version allégée de BERT :

- plus rapide
- mais moins performant sur des tâches complexes

## 4. Conclusion

Les faibles performances sont dues :

- à la nature extractive du modèle
- à la limite de tokens
- aux capacités réduites de DistilBERT

