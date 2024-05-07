class Animation:
    def __init__(self, images, img_dur = 10, loop = True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.frame = 0
        self.currentAnimIdx = 0

    def update(self):
        self.frame += 1
        if self.frame == self.img_duration:
            self.frame = 0
            print(self.currentAnimIdx)
            self.currentAnimIdx += 1
            print(self.currentAnimIdx)
            if self.currentAnimIdx > len(self.images) - 1:
                self.currentAnimIdx = 0
        return self.images[self.currentAnimIdx]
