from protopost import ProtoPost

#simple route that just returns apples * bananas
ProtoPost({
  "": lambda data: data["apples"] * data["bananas"]
}).start(80)
