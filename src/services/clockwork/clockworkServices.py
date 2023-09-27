# Dokumentation https://docs.herocoders.com/clockwork/use-the-clockwork-api
def authentification(token: str):
    header ={
        "Authorization": f"Basic {token}"
    }
    return header

def createCall(clockworkEndpoint):
    # API-Endpunkt und Header-Informationen
    url = f"https://api.clockwork.report/v1/{clockworkEndpoint}}"
    return url



if __name__ == "__main__":
    authentification("3km31746G/4twG2/BZj6KPWA35+t+c1lJ3NCCg3p6VMpo5vK2xyxDdYo8zFJoDUyMMBGRyYHQef6a7eQPThydNCYYnKSHEdI8hPx/Q==--07v6lPkTJNyXMhR/--SewUbFOiyAI/2+8NnjWdCQ==")
    createCall("worklogs")