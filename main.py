import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

# Setup
WP_URL = "YOUR_WORDPRESS_SITE_URL/xmlrpc.php"
WP_USERNAME = "YOUR_WP_USERNAME"
WP_PASSWORD = "YOUR_WP_PASSWORD"

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

# Fetch content from OpenAI with structure
def generate_content(topic):
    prompt = f"""
    Create a structured, SEO-friendly blog post on the topic: {topic}.
    [Header]: {topic}
    [Subheader]: Introduction
    [Body]: {{Introduction content here...}}

    [Subheader]: Background
    [Body]: {{Background content here...}}

    [Subheader]: Key findings
    [Body]: {{Key findings content here...}}

    [Subheader]: Conclusion
    [Body]: {{Conclusive thoughts...}}
    """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1500
    )
    return response.choices[0].text.strip()

# Present content to user and verify
def verify_content(content):
    print(content)
    verification = input("Is this content okay to post? (yes/no): ").strip().lower()
    return verification == "yes"

# Convert structured content to HTML format
def format_for_wordpress(content):
    content = content.replace('[Header]:', '<h1>')
    content = content.replace('[Subheader]:', '<h2>')
    content = content.replace('[Body]:', '<p>')
    
    content = content.replace('<h1>', '</h1><h1>')
    content = content.replace('<h2>', '</h2><h2>')
    content = content.replace('<p>', '</p><p>')
    
    content = content.replace('</h1><h1>', '<h1>', 1)
    content = content.replace('</h2><h2>', '<h2>', 1)
    content = content.replace('</p><p>', '<p>', 1)

    content += "</p>"
    return content

# Post to WordPress
def post_to_wordpress(title, content):
    client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = 'publish'
    post_id = client.call(posts.NewPost(post))
    return post_id

if __name__ == "__main__":
    topic = input("Enter the science topic: ").strip()
    raw_content = generate_content(topic)
    
    if verify_content(raw_content):
        formatted_content = format_for_wordpress(raw_content)
        post_id = post_to_wordpress(topic, formatted_content)
        print(f"Post published with ID: {post_id}")
    else:
        print("Content was not posted.")
