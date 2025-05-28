import jinja2 as jinja


def main():
    env = jinja.Environment(
        loader=jinja.FileSystemLoader("templates")
    )
    template = env.get_template('article.html')
    print(template.render(article_name='article_name'))


if __name__ == "__main__":
    main()
