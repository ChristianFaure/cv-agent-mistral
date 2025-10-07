import streamlit as st
from mistralai import Mistral
import os

# Configuration de la page
st.set_page_config(
    page_title="CV Interactif - [Votre Nom]",
    page_icon="🤖",
    layout="wide"
)

# Initialisation du client Mistral
@st.cache_resource
def get_mistral_client():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("⚠️ MISTRAL_API_KEY non trouvée. Vérifiez vos secrets Streamlit.")
        st.stop()
    return Mistral(api_key=api_key)

client = get_mistral_client()

# Votre CV et contexte (à enrichir avec vos vraies données)
CV_CONTEXT = """
Je suis [VOTRE NOM], candidat pour le poste de Head of Applied AI & Strategic Accounts chez Mistral AI.

## EXPÉRIENCE CLÉS

### OCTO TECHNOLOGY (2012-2024)
- Managing Partner & Directeur Scientifique
- Management de 100 ingénieurs sur sujets d'innovation
- Direction de transformations digitales majeures : Accor (refonte moteur réservation), 
  Club Med (réorg tech/produit), Engie (8 plateformes, DDD, DORA), BNP Paribas (priorisation portfolio)
- Directeur Scientifique : 7 thèses CIFRE avec INRIA/CEA/CNRS, CIR 1,6M€
- Due diligence tech pour VCs (Criteo, Naxicap, Partech)
- CTO interim chez lesfurets.com

### ATOS/CAPGEMINI (1999-2012)
- Senior Manager sur projets innovation (Web 2.0, API, Agile)

## THOUGHT LEADERSHIP
- Président Institut de Recherche et Innovation (Centre Pompidou) 2010-2018
- Membre CA Ars Industrialis (association Bernard Stiegler) 2006-2020
- Co-auteur livre avec Bernard Stiegler sur philosophie de la technique
- Enseignement UTC : Histoire et Prospective des Industries Culturelles

## COMPÉTENCES
- Scaling d'équipes tech (20 → 100 personnes)
- Transformations B2B grands comptes
- R&D appliquée (thèses CIFRE, innovation)
- Philosophie de la technique, épistémologie
- Vision européenne de l'IA responsable

## MA VISION POUR MISTRAL AI
Je veux structurer l'équipe Applied AI avec 3 piliers :
1. OPÉRATIONNEL (50%) : Industrialiser les POCs, créer des playbooks réutilisables
2. STRATÉGIQUE (20%) : Développer des secteurs verticaux (jeux vidéo, industries culturelles)
3. THOUGHT LEADERSHIP (30%) : Porter la vision européenne de l'IA, relations institutionnelles

Mon atout différenciant : je traduis la technologie de pointe en valeur business B2B.
Je ne suis pas expert ML, mais je sais manager des équipes plus expertes que moi et structurer l'adoption.

## RÉALISATIONS QUANTIFIABLES
- 100 ingénieurs managés
- 20+ projets de transformation majeurs
- 7 thèses CIFRE menées à terme
- Taux satisfaction client >90%
- Président institut de recherche public
"""

# Interface utilisateur
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF7000 0%, #FF9040 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background: #f0f0f0;
        border-left: 4px solid #FF7000;
    }
    .assistant-message {
        background: #FFF5ED;
        border-left: 4px solid #FF7000;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="main-header">
    <h1>🤖 CV Agent Conversationnel</h1>
    <h2>[Votre Nom] - Candidat Head of Applied AI chez Mistral AI</h2>
    <p>Posez-moi n'importe quelle question sur mon parcours, mes compétences ou ma vision pour Mistral AI !</p>
</div>
""", unsafe_allow_html=True)

# Colonnes
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Conversation")
    
    # Initialisation de l'historique
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Message de bienvenue
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Bonjour ! Je suis l'agent conversationnel du CV de [Votre Nom]. Je peux répondre à toutes vos questions sur son parcours, ses compétences, et sa vision pour le poste de Head of Applied AI chez Mistral AI. Que souhaitez-vous savoir ?"
        })
    
    # Affichage de l'historique
    for message in st.session_state.messages:
        css_class = "user-message" if message["role"] == "user" else "assistant-message"
        role_name = "Vous" if message["role"] == "user" else "Agent CV"
        st.markdown(f'<div class="chat-message {css_class}"><strong>{role_name}:</strong> {message["content"]}</div>', 
                   unsafe_allow_html=True)
    
    # Input utilisateur
    user_input = st.chat_input("Posez votre question...")
    
    if user_input:
        # Ajouter message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Construire le prompt pour Mistral
        system_prompt = f"""Tu es un assistant qui répond aux questions sur le CV et le profil professionnel d'un candidat.

Contexte du candidat :
{CV_CONTEXT}

Instructions :
- Réponds de manière naturelle et conversationnelle
- Utilise "je" pour parler du candidat (tu ES le candidat)
- Sois précis avec les chiffres et les faits
- Si on te demande quelque chose qui n'est pas dans le contexte, dis-le honnêtement
- Mets en avant les réalisations concrètes
- Reste professionnel mais accessible
- Si la question porte sur la motivation pour Mistral AI, explique clairement la proposition de valeur unique
"""
        
        # Préparer les messages pour l'API (nouveau format)
        api_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Ajouter l'historique (garder les 6 derniers messages pour le contexte)
        for msg in st.session_state.messages[-6:]:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Appel à l'API Mistral (nouvelle syntaxe)
        try:
            with st.spinner("🤔 Réflexion en cours..."):
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=800
                )
                
                assistant_response = response.choices[0].message.content
                
                # Ajouter la réponse à l'historique
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
                # Rerun pour afficher la nouvelle réponse
                st.rerun()
        
        except Exception as e:
            st.error(f"Erreur : {str(e)}")
            st.info("💡 Astuce : Assurez-vous que MISTRAL_API_KEY est défini dans vos secrets Streamlit")

with col2:
    st.subheader("📋 Actions rapides")
    
    st.markdown("### 💡 Questions suggérées")
    suggestions = [
        "Quelle est ton expérience en management d'équipes tech ?",
        "Pourquoi Mistral AI ?",
        "Quelle serait ta première action en tant que Head of Applied AI ?",
        "Parle-moi de tes transformations chez OCTO",
        "Comment articules-tu philosophie et technologie ?",
        "Quelle est ta vision du fine-tuning en B2B ?",
        "Que penses-tu du secteur des jeux vidéo pour Mistral ?",
        "Comment as-tu géré la R&D chez OCTO ?"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📥 Téléchargements")
    st.button("📄 CV PDF complet", help="Télécharger le CV au format PDF")
    st.button("📧 Me contacter", help="Envoyer un email")
    st.button("🔗 LinkedIn", help="Voir mon profil LinkedIn")
    
    st.markdown("---")
    st.markdown("### 🎯 À propos")
    st.info("""
    Cet agent conversationnel utilise l'API Mistral AI pour répondre 
    à vos questions sur mon profil professionnel.
    
    **Technologie :**
    - Modèle : Mistral Large
    - Framework : Streamlit
    - Contexte : CV + vision stratégique
    
    Une démonstration concrète de ma compréhension de l'Applied AI ! 🚀
    """)
    
    # Statistiques (à développer)
    if len(st.session_state.messages) > 1:
        st.markdown("---")
        st.metric("Questions posées", len([m for m in st.session_state.messages if m["role"] == "user"]))
