import reddit_twitter_bot


def check_sub(title, expected):
    actual = reddit_twitter_bot._substitute_handles(title)
    if actual != expected:
        print("input:", title)
        print("actual:", actual)
        print("expected:", expected)
        assert actual == expected


check_sub("PSG.LGD", "@PSGeSports.@LGDgaming")
check_sub("Miracle and Ana", "@NigmaMiracle and @anadota99")
check_sub("Announcement by Team Secret", "Announcement by @teamsecret")
check_sub(
    "EG invited to ESL One Hamburg", "@EvilGeniuses invited to @ESLDota2 One Hamburg"
)
check_sub("Kpii has left Newbee", "@kpiidota has left @NewbeeCN")
check_sub("Everything N0tail has said", "Everything @OG_BDN0tail has said")
check_sub("Dota 2", "@DOTA2")
check_sub("Dota", "@DOTA2")
check_sub("Dota2", "@DOTA2")
check_sub("Stan", "@StanCifka")

print("Success!")
