class Animation:
    def __init__(self, images, img_dur = 12):
        self.images = images
        self.img_duration = img_dur
        self.frame = 0
        self.currentAnimIdx = 0

    def update(self):
        self.frame += 1
        if self.frame >= self.img_duration:
            self.frame = 0
            self.currentAnimIdx += 1
        if self.currentAnimIdx >= len(self.images) - 1:
                self.currentAnimIdx = 0
        return self.images[self.currentAnimIdx]

    def change_image(self, images, image_dur = 12):
        self.images = images
        self.img_duration = image_dur