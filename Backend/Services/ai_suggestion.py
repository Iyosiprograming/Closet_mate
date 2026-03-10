async def get_suggestion(prompt):
    print("get_suggestion called with", prompt  )
    return {"suggestion":"This is a dummy suggestion "+ prompt}