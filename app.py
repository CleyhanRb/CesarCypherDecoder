import threading
import queue
import time

original = open("original.txt", "r").read()
liste = open(
    "liste.txt",
    "r",
    encoding="utf-8",
).read()

tab = original.replace("\n", " ").split(" ")

lettersMin = "abcdefghijklmnopqrstuvwxyz"
lettersMaj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decodeWord(word, code):
    decoded = ""
    for c in word:
        if c in lettersMin:
            decoded += lettersMin[(lettersMin.index(c) + code) % 26]
        elif c in lettersMaj:
            decoded += lettersMaj[(lettersMaj.index(c) + code) % 26]
        else:
            decoded += c

    return decoded


def sentenceRate(sentence: list, queue: queue.Queue = queue.Queue()):
    nb = 0
    for w in sentence:
        if (
            str(w)
            .replace(".", "")
            .replace(",", "")
            .replace("!", "")
            .replace("?", "")
            .replace(";", "")
            .replace(":", "")
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            in liste
        ):
            nb += 1

    return round(100 * nb / len(sentence), 1)


def decodeSentence(s, code, queue: queue.Queue = queue.Queue()):
    sentence = []
    for w in s:
        sentence.append(decodeWord(w, code))

    queue.put((code, sentence, sentenceRate(sentence)))


def main():
    sentences = []
    q = queue.Queue()
    threads = []

    before = time.time()

    for i in range(1, 26):

        t = threading.Thread(target=decodeSentence, args=(tab, i, q))
        t.start()
        threads.append(t)
        print(f"{round(100*i/25)}%", end=" ")
        # sentence = [decodeWord(w, i) for w in tab]

    print()

    for i in range(len(threads)):
        print(f"{round(100*i/len(threads))}%", end=" ")
        threads[i].join()

    sentences = [q.get() for t in threads]
    sentences.sort(key=lambda x: x[2], reverse=True)

    after = time.time()

    # sentences.append((i, sentence, sentenceRate(sentence)))
    # sentences.sort(key=lambda x: x[2], reverse=True)

    # print(
    #     f"\nWinner:\nKey: {sentences[0][0]}\nScore: {sentences[0][2]}\nDecoded: {" ".join(sentences[0][1])}"
    # )
    print(
        f"\nWinner:\nKey: {sentences[0][0]}\nScore: {sentences[0][2]}\nTime: {round(after - before, 2)}s"
    )
    out = open(
        "out.txt",
        "w",
    )

    out.write(" ".join(sentences[0][1]))


main()
