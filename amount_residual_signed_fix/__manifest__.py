{
    "name": "Fix Amount Due",
    "description": """Fixes a discrepancy between amount_residual_signed and amount_residual field on Account Move.""",
    "version": "15.0.0.1",
    "license": "Other proprietary",
    "author": "Bemade Inc.",
    "contributors": ["Marc Durepos <marc@bemade.org>"],
    "category": "Accounting",
    "depends": [
        "account",
    ],
    "demo": [],
    'data': [
    ],
    'test': [],
    'installable': True,
    'active': False,
    'post_init_hook': '_post_init',
}
