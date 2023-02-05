import pprint

from pytactx import Agent

if __name__ == '__main__':
    agent = Agent("QQ")
    pprint.pprint(agent.jeu)
    print("\n"*3)
    pprint.pprint(agent.profile)
    print("\n"*3)
    pprint.pprint(agent.topicGameRead)
    print("\n"*3)
    pprint.pprint(agent.topicAgentRead)
