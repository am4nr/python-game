import pygame

def trim_surface(surface, border_color=(255, 255, 255), border_size=2):
    # Create a mask from the surface's alpha channel
    mask = pygame.mask.from_surface(surface)
    
    # Find the bounding rectangle of the non-transparent areas
    if mask.get_bounding_rects():
        rect = mask.get_bounding_rects()[0]
    else:
        # If the mask is completely transparent, return the original surface
        return surface
    
    # Create a new surface with the size of the bounding rectangle
    trimmed_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    trimmed_surface.blit(surface, (0, 0), rect)

    # Create a new surface to hold the bordered image
    bordered_surface = pygame.Surface(
        (trimmed_surface.get_width() + 2 * border_size, 
         trimmed_surface.get_height() + 2 * border_size), 
        pygame.SRCALPHA
    )
    
    # Fill with transparent background
    bordered_surface.fill((0, 0, 0, 0))
    
    # Draw the border
    pygame.draw.rect(bordered_surface, border_color, bordered_surface.get_rect(), border_size)
    
    # Blit the trimmed surface onto the bordered surface
    bordered_surface.blit(trimmed_surface, (border_size, border_size))
    
    return bordered_surface

