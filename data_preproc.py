import codecs, json, re
from random import shuffle
import os

# data directory: https://nijianmo.github.io/amazon/index.html

data_dir = "/data/users/chandlerzuo/llm_finetune_projects/rlhf_recsys"

# key: productID，value: title
games = {}
cc = 0

with codecs.open(f"{data_dir}/src_data/meta_Video_Games.json", mode="r") as fin:
    for line in fin:
        tmp_info = json.loads(line.strip())
        # asin - ID of the product
        # title - name of the product
        games[tmp_info["asin"]] = tmp_info["title"]
        if len(games) % 10000 == 0:
            print(f"Length of games: {len(games)}")


# key: userid, value: rating
user_reviews = {}

cc = 0
with codecs.open(f"{data_dir}/src_data/Video_Games_5.json", mode="r") as fin:
    for line in fin:
        tmp_info = json.loads(line.strip())

        # reviewerID - ID of the reviewer
        reviewer_id = tmp_info["reviewerID"]

        time_info = re.split(", | ", tmp_info["reviewTime"])
        review_time = time_info[2] + "-" + time_info[0] + "-" + time_info[1]

        # asin - ID of the product
        product_id = tmp_info["asin"]

        # overall - rating of the product
        rating = tmp_info["overall"]

        # if cc > 1000:
        #     break

        # print(tmp_info)
        # print(user_reviews)

        if product_id in games.keys():
            product_title = games[product_id]

            if reviewer_id in user_reviews.keys():
                user_reviews[reviewer_id].append((product_title, rating, review_time))
            else:
                user_reviews[reviewer_id] = [(product_title, rating, review_time)]

        if len(user_reviews) % 10000 == 0:
            print(f"Length of user_reviews: {len(user_reviews)}")

        cc += 1

user_reviews_sorted = {}
for k, v in user_reviews.items():
    # dedup
    v = list(set(v))
    # order the ratings from the same user by time
    v_sorted = sorted(v, key=lambda x: x[2])
    # only keep long user histories
    if len(v) >= 7:
        # print(f'v: {v}, v_sorted: {v_sorted}')
        user_reviews_sorted[k] = v_sorted
print(f"Length of user_reviews_sorted: {len(user_reviews_sorted)}")

# total sample size
samples = []
# instruction
instruction = 'You are an assistant working on Video Games recommendations. Given the user\'s history of Video Games they have shopped, which includes the "Title" of the Video Games and the "Rating" the user rate (the Rating value is like or dislike), please decide whether the user likes to shop the target Video Games by outputting the order of their titles.'

samples = []
cc = 0
for k, v in user_reviews_sorted.items():
    # print('-'*10)
    # print(v)
    sample_input = "User shopped Video Games histories (Title and Rating): \n"
    # Use the first N-2 ratings as history
    for vv in v[0:-2]:
        # binarize the rating
        if vv[1] > 3.0:
            rating = "like"
        else:
            rating = "dislike"
        sample_input += "<Title: {}, Rating: {}>\n".format(vv[0], rating)

    sample_input += "Based on the Video Games histories, please sort the following two Video Games titles. The one in the front is what the user like and should be recommended to user: \n"

    # the last 2 ratings are the target
    sample_input += "<Title: " + v[-2][0] + ">\n"
    sample_input += "<Title: " + v[-1][0] + ">\n"

    # print(f'v[-1][1]: {v[-1][1]}, v[-2][1]: {v[-2][1]}')
    # For RLHF, keep only the samples where the user's last two ratings are different
    if (v[-1][1] > 3.0 and v[-2][1] <= 3.0) or (v[-1][1] <= 3.0 and v[-2][1] > 3.0):
        # print(f'v[-1][1] != v[-2][1]: {v[-1][1]}, {v[-2][1]}')
        if v[-1][1] > v[-2][1]:
            # like
            option1 = v[-1][0]
            # dislike
            option2 = v[-2][0]
        else:
            # like
            option1 = v[-2][0]
            # dislike
            option2 = v[-1][0]

        # chosen: liked is before disliked
        chosen = "<Title: " + option1 + ">\n" + "<Title: " + option2 + ">"
        # rejected: disliked is before liked
        rejected = "<Title: " + option2 + ">\n" + "<Title: " + option1 + ">"

        sample = {
            "instruction": instruction,
            "input": sample_input,
            "chosen": chosen,
            "rejected": rejected,
        }
        # print(f'--------')
        # print(v)
        # print(sample)
        samples.append(sample)

        if len(samples) % 10000 == 0:
            print(f"Length of samples: {len(samples)}")

    # cc += 1
    # if cc > 10:
    #     break

print(f"Length of samples: {len(samples)}")


print(samples[0:10])

# split between train and validation
shuffle(samples)

train = samples[: int(len(samples) * 0.8)]
test = samples[int(len(samples) * 0.8) :]

print(
    f"sample size: {len(samples)}, train sample size: {len(train)}, test sample size: {len(test)}"
)

try:
    os.mkdir(f"{data_dir}/processed")
except FileExistsError:
    pass


with open(f"{data_dir}/processed/rlhf_train.json", "w", encoding="utf-8") as save_file:
    json.dump(train, save_file, indent=4)

with open(f"{data_dir}/processed/rlhf_test.json", "w", encoding="utf-8") as save_file:
    json.dump(test, save_file, indent=4)  # , sort_keys=True
