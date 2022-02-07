import arq_wait
import arq_repeat
import arq_gbn

def main():
    PACKAGES = 5

    arq_wait.start(PACKAGES)
    arq_repeat.start(PACKAGES)
    arq_gbn.start(PACKAGES)


if __name__ == '__main__':
    main()
