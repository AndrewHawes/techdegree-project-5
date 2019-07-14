test_users = [
    {
        "username": "Andrew",
        "email": "andrew@test.com",
        "password": "password",
        "is_admin": 1
    },
    {
        "username": "Kyle_Murphy",
        "email": "kyle@test.com",
        "password": "password",
        "is_admin": 0
    },
    {
        "username": "Robert",
        "email": "robert@test.com",
        "password": "password",
        "is_admin": 0
    },
    {
        "username": "Admin",
        "email": "admin@test.com",
        "password": "password",
        "is_admin": 1
    }
]

test_entries = [
    {
        "title": "First Entry",
        "time": 1,
        "learned": "I learned something, and I'm going to type a second line "
                   "after I finish this sentence.\n"
                   "Here's the second line. Now there's going to be a third.\n"
                   "This is the third.",
        "resources": "resource1\nhttp://www.test.com\n"
                     "resource2",
        "user_id": 1,
        "tags": "test"
    },
    {
        "title": "Ninjas",
        "time": 20,
        "learned": "Ninjas are mammals.",
        "resources": "http://www.realultimatepower.net/index4.htm\r\nhttps://en.wikipedia.org/wiki/Mammal\r\nReal Ultimate Power",
        "user_id": 3,
        "tags": "ninjas mammals"
    },
    {
        "title": "Ninjas!",
        "time": 2,
        "learned": "This is another entry about ninjas, but this time it has an exclamation point!",
        "resources": "",
        "user_id": 3,
        "tags": "ninjas punctuation slugs"
    },
    {
        "title": "Slugs",
        "time": 10,
        "learned": "Slugs are jerks and lack the dexterity to become ninjas.",
        "resources": "https://en.wikipedia.org/wiki/Slug\r\nhttp://www.realultimatepower.net/index4.htm",
        "user_id": 3,
        "tags": "slugs ninjas"
    },
    {
        "title": "Slugs?",
        "time": 2,
        "learned": "Testing to see if slug gets screwed up.",
        "resources": "",
        "user_id": 3,
        "tags": "slugs punctuation"
    },
    {
        "title": "Test Entry Kyle",
        "time": 1,
        "learned": "This is a test entry.",
        "resources": "https://www.python.org\r\n",
        "user_id": 2,
        "tags": "test"
    },
    {
        "title": "Test Entry That Has Nothing to Do With Mammals",
        "time": 20,
        "learned": "This entry has nothing to do with mammals.\r\n\r\nI'm very tired.",
        "resources": "Unisom",
        "user_id": 2,
        "tags": "test mammals insomnia"
    }
]
