# ATLAS

**A self-hosted platform for developing, deploying, and monitoring algorithmic trading strategies.**

The platform is designed to run on a local machine or server, with team members accessing the same instance through their browsers.

See [Project Documentation](https://docs.google.com/document/d/1xfD-a51XLQYDKf0SW4yrSjkkpkeMbbOo0Hi6VfGp0M4/edit?usp=sharing) for architecture details.

### Getting Started with Development

I recommend doing it in your root

```bash
git clone https://github.com/umn-adc/ATLAS.git
cd ATLAS
```
### Backend - Native Python

From the backend directory:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Contributing

ATLAS is developed by members of the University of Minnesota App Developers Club.

### Development Workflow

1. Find or claim an issue on the GitHub project board.
2. Read the relevant module and documentation.
3. Create a branch for your work.
4. Implement the change and add appropriate tests.
5. Open a pull request.
6. Address review feedback before merging.

Keep pull requests focused on a single issue whenever possible.

## Documentation

Project documentation is maintained with MkDocs.

Documentation covers architecture, development setup, module interfaces, and contributor onboarding as these areas are developed.

## License
GPLv3
