from flask import Blueprint, render_template, request, current_app

main_routes = Blueprint("main", __name__)

# ------------------------
# HOME
# ------------------------
@main_routes.route("/")
def main():
    """
    Renders the main page of the web application.
    """
    return render_template("index.html")


# ------------------------
# QUERY
# ------------------------
@main_routes.route("/query", methods=["GET", "POST"])
def query():
    """
    Handles natural language queries through the Query Agent.
    Supports both viewing the query form (GET) and submitting a question (POST).
    """
    answer = None

    if request.method == "POST":
        # Extract the question from the form submission
        question = request.form.get("question")
        # Access the shared Query Agent from the app config
        agent = current_app.config["query_agent"]

        # Process the question and extract the generated answer
        result = agent.ask(question)
        answer = result.get("answer")

    return render_template("query.html", answer=answer)


# ------------------------
# PERSONALIZATION
# ------------------------
@main_routes.route("/personalization", methods=["GET", "POST"])
def personalization():
    """
    Manages user personas and personalized recommendations.
    Handles persona creation and recommendation generation based on form actions.
    """
    recommendations = None

    # Access the shared Personalization Agent
    agent = current_app.config["personalization_agent"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            # Create a new user persona with explicit preferences
            user_id = request.form.get("user_id")
            prefs = {
                "preferred_categories": request.form.getlist("categories"),
                "budget_range": request.form.get("budget"),
                "preferred_brands": request.form.getlist("brands")
            }
            agent.create_user_persona(user_id, prefs)

        elif action == "recommend":
            # Generate recommendations for an existing user persona
            user_id = request.form.get("user_id")
            recommendations = agent.get_personalized_recommendations(user_id)

    return render_template("personalization.html", recommendations=recommendations)


# ------------------------
# TRANSFORMATION
# ------------------------
@main_routes.route("/transformation", methods=["GET", "POST"])
def transformation():
    """
    Handles data enrichment tasks through the Transformation Agent.
    Allows adding summaries and tags to products via the web interface.
    """
    message = None
    # Access the shared Transformation Agent
    agent = current_app.config["transformation_agent"]

    if request.method == "POST":
        product = request.form.get("product")

        # Check if the user is submitting a new summary
        if "summary" in request.form:
            summary = request.form.get("summary")
            agent.add_product_summary(product, summary)
            message = "Summary added!"

        # Check if the user is submitting new tags
        if "tags" in request.form:
            tags = request.form.get("tags").split(",")
            agent.add_product_tags(product, tags)
            message = "Tags added!"

    return render_template("transformation.html", message=message)