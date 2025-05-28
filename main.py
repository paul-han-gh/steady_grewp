import jinja2 as jinja


def main():
    env = jinja.Environment(
        loader=jinja.FileSystemLoader("templates")
    )
    template = env.get_template('header.html')
    print(template.render())


if __name__ == "__main__":
    main()
