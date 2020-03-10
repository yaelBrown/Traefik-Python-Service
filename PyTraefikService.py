import requests
import json

class PyTraefikService:
    demoURL = 'https://demo.glyptodon.com/'

    example = {
        "frontends": {
        "frontend2": {
            "routes": {
            "test_2": {
                "rule": "Path:/test"
            }
            },
            "backend": "backend1"
        },
        "frontend1": {
            "routes": {
            "test_1": {
                "rule": "Host:test.localhost"
            }
            },
            "backend": "backend2"
        }
        },
        "backends": {
        "backend2": {
            "loadBalancer": {
            "method": "drr"
            },
            "servers": {
            "server2": {
                "weight": 2,
                "URL": "http://172.17.0.5:80"
            },
            "server1": {
                "weight": 1,
                "url": "http://172.17.0.4:80"
            }
            }
        },
        "backend1": {
            "loadBalancer": {
            "method": "wrr"
            },
            "circuitBreaker": {
            "expression": "NetworkErrorRatio() > 0.5"
            },
            "servers": {
            "server2": {
                "weight": 1,
                "url": "http://172.17.0.3:80"
            },
            "server1": {
                "weight": 10,
                "url": "http://172.17.0.2:80"
            }
            }
        }
        }
    }

    def readExampleFile():
        return open("example-config.json", "r").read()

    """
    Returns a SINGLE dictionary of config used for Traefik
        FE_Path = '/{range_id}/{operator_id}'
            Must include leading '/', ex.: '/1/1' 
        BE_Path = 'https://demo.glyptodon.com/#/client/ZGVtbwBjAGRlbW8='
            Full address to guacamole machine
    """
    def addSingleConfig(FE_Path="", BE_Path="", pathCnt=1):
        if FE_Path[0] != "/":
            FE_Path = "".join(("/", FE_Path))
        
        config = {
            "frontends": {
                "FE_Operator_Path": {
                    "routes": {
                        f"route_{pathCnt}": {
                            "rule": f"Path:{FE_Path}"
                        }
                    },
                    "backend": f"backend_{pathCnt}"
                }
            },
            "backends": {
                f"backend_{pathCnt}": {
                    "servers": {
                        f"server_{pathCnt}": BE_Path
                    }
                }
            }
        }
        return config

    """
    Returns a list of multiple dictionaries of configs
    """
    def addMultipleConfigs(cfgs):
        if type(cfgs) != list:
            return "That is not a list!"
        else:
            cnt = 1
            out = []
            for c in cfgs:
                print(c)
                out.append(PyTraefikService.addSingleConfig(c['FE_Path'], c['BE_Path'], str(cnt)))
                cnt += 1
            return out

    """
    Sends a request to Traefik to make changes to config
        url = address to Traefik
        cfg = dictionary of config to send to Traefik
        addOrRem = Decides the direction of data to Traefik
            True = adds by sending PUT request
            False = removes by sending DELETE request
    """
    def putToTraefik(cfg, addOrRem, url="http://localhost:8080/api/providers/rest"):
        if type(cfg) != list:
            pass
        elif addOrRem == None or type(addOrRem) != bool:
            print("addOrRem must be a present and a boolean")
            return "addOrRem must be a present and a boolean"
        print("is this going to work?")
        cfg = json.dumps(PyTraefikService.readExampleFile())
        print(cfg)
        if addOrRem == True: 
            res = requests.put(url, data = cfg, headers={'Content-Type': 'application/json'})
            if res.status_code == 200:
                print("Successfully added data to Traefik!")
                return "Successfully added data to Traefik!"
            else:
                print(f"Unable to add to Traefik: {res.status_code}")
                return f"Unable to add to Traefik: {res.status_code}"
        else: 
            res = requests.delete(url, data = cfg)
            if res.status_code == 200:
                print("Successfully deleted data from Traefik!")
                return "Successfully deleted data from Traefik!"
            else:
                print(f"Unable to add to Traefik: {res.status_code}")
                return f"Unable to add to Traefik: {res.status_code}"

# test above methods
aa = [1,3,4,5]

# print(PyTraefikService.addMultipleConfigs("aa"))

bb = [
    {
        "FE_Path": "/1/1",
        "BE_Path": "http://www.redhat.com"
    },
    {
        "FE_Path": "/1/2",
        "BE_Path": PyTraefikService.demoURL
    }
]

cc = {
    "FE_Path": "/1/3",
    "BE_Path": "http://www.newegg.com"
}

fe = "/1/3"
be = "http://www.amazon.com"

# print(PyTraefikService.addSingleConfig("/2/1", "http://www.stackoverflow.com"))
# print(PyTraefikService.addMultipleConfigs(bb))
# PyTraefikService.putToTraefik(PyTraefikService.addMultipleConfigs(bb), True)
# PyTraefikService.putToTraefik(PyTraefikService.addSingleConfig(fe, be), True)
PyTraefikService.putToTraefik(json.dumps(PyTraefikService.example), True)


# PyTraefikService.addSingleConfig(fe, be)

# print(PyTraefikService.readExampleFile())